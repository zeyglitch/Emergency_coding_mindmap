# -*- coding: utf-8 -*-

from pyvis.network import Network
import tempfile


def safe_text(txt):
    """
    Nettoyage texte pour éviter erreurs encodage Windows
    """
    try:
        return str(txt).encode("utf-8", "ignore").decode("utf-8")
    except Exception:
        return str(txt)


def get_node_style(level):
    """
    Styles visuels par niveau hiérarchique
    """
    styles = {
        "organe": {"color": "#ff6b6b", "size": 30},
        "type": {"color": "#f7b267", "size": 22},
        "inter": {"color": "#4dabf7", "size": 18},
        "definition": {"color": "#74c69d", "size": 14},
        "code": {"color": "#adb5bd", "size": 12}
    }
    return styles.get(level, {})


def generate_mindmap(df, search=""):
    """
    Génère une carte mentale interactive optimisée
    """

    # ✅ IMPORTANT : inline JS pour éviter erreur vis.js
    net = Network(
        height="100vh",
        width="100%",
        directed=True,
        notebook=False,
        cdn_resources="in_line"
    )

    # ✅ Options de physique optimisées (cluster en étoile)
    net.set_options("""
    {
      "interaction": {
        "hover": true
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -8000,
          "centralGravity": 0.1,
          "springLength": 350,
          "springConstant": 0.04,
          "damping": 0.09,
          "avoidOverlap": 1.0
        },
        "solver": "barnesHut",
        "stabilization": {
          "enabled": true,
          "iterations": 300
        }
      }
    }
    """)

    # ✅ Performance
    df = df.drop_duplicates()
    df = df.head(2000)  # limite sécurité

    added_nodes = set()
    added_edges = set()

    for _, row in df.iterrows():

        o = safe_text(row["organe"])
        t = safe_text(row["type_atteinte"])
        i = safe_text(row["intermediaire"])
        d = safe_text(row["definition"])
        c = safe_text(row["code"])

        # ----------- NODES -----------

        if o not in added_nodes:
            net.add_node(o, label=o, **get_node_style("organe"))
            added_nodes.add(o)

        if t not in added_nodes:
            net.add_node(t, label=t, **get_node_style("type"))
            added_nodes.add(t)

        if i not in added_nodes:
            net.add_node(i, label=i, **get_node_style("inter"))
            added_nodes.add(i)

        if d not in added_nodes:
            net.add_node(d, label=d[:60], **get_node_style("definition"))
            added_nodes.add(d)

        if c not in added_nodes:
            net.add_node(
                c,
                label=c,
                title=f"""
Organe: {o}
Type: {t}
Intermédiaire: {i}
Définition: {d}
Code: {c}
""",
                **get_node_style("code")
            )
            added_nodes.add(c)

        # ----------- EDGES -----------

        edges_to_add = [(o, t), (t, i), (i, d), (d, c)]
        for src, dst in edges_to_add:
            edge_id = f"{src}|||{dst}"
            if edge_id not in added_edges:
                net.add_edge(src, dst)
                added_edges.add(edge_id)

    # ✅ Création fichier temporaire
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    
    # ✅ Génération HTML sans écrire avec save_graph pour éviter les erreurs d'encodage 'charmap' sous Windows
    html = net.generate_html(notebook=False)

    # ✅ JS interaction, centrage + surlignage + Focus Voisinage
    js = """
<script>
document.addEventListener("DOMContentLoaded", function() {

    // 1. Sauvegarder les couleurs et styles d'origine
    var allNodes = nodes.get();
    var originalNodes = {};
    for(var i=0; i<allNodes.length; i++) {
        originalNodes[allNodes[i].id] = {
            color: allNodes[i].color || "#97C2FC",
            fontColor: (allNodes[i].font && allNodes[i].font.color) ? allNodes[i].font.color : "black"
        };
    }

    var allEdges = edges.get();
    var originalEdges = {};
    for(var i=0; i<allEdges.length; i++) {
        originalEdges[allEdges[i].id] = allEdges[i].color || {color: "#848484"};
    }

    // 2. Arrêter la physique après la stabilisation
    network.once("stabilizationIterationsDone", function() {
        network.setOptions( { physics: false } );
    });

    // 3. Clic sur un noeud -> Envoi vers Python + Effet de focus (Arbre complet)
    network.on("click", function (params) {
        var updateNodes = [];
        var updateEdges = [];

        if (params.nodes.length > 0) {
            var nodeId = params.nodes[0];
            window.location.href = "pyvis://click?node=" + encodeURIComponent(nodeId);

            var relatedNodes = new Set([nodeId]);
            var allEdgesArr = allEdges;

            // Fonction récursive pour trouver les ancêtres (remonter à la racine)
            function getAncestors(id) {
                for (var i = 0; i < allEdgesArr.length; i++) {
                    if (allEdgesArr[i].to === id && !relatedNodes.has(allEdgesArr[i].from)) {
                        relatedNodes.add(allEdgesArr[i].from);
                        getAncestors(allEdgesArr[i].from);
                    }
                }
            }

            // Fonction récursive pour trouver les descendants (tout ce qui suit)
            function getDescendants(id) {
                for (var i = 0; i < allEdgesArr.length; i++) {
                    if (allEdgesArr[i].from === id && !relatedNodes.has(allEdgesArr[i].to)) {
                        relatedNodes.add(allEdgesArr[i].to);
                        getDescendants(allEdgesArr[i].to);
                    }
                }
            }

            getAncestors(nodeId);
            getDescendants(nodeId);

            // Mise à jour des Noeuds
            for (var i = 0; i < allNodes.length; i++) {
                var n = allNodes[i];
                if (relatedNodes.has(n.id)) {
                    updateNodes.push({
                        id: n.id, 
                        color: originalNodes[n.id].color,
                        font: {color: originalNodes[n.id].fontColor}
                    });
                } else {
                    updateNodes.push({
                        id: n.id, 
                        color: "rgba(200,200,200,0.25)",
                        font: {color: "rgba(150,150,150,0.4)"}
                    });
                }
            }

            // Mise à jour des Liens (Edges)
            for (var i = 0; i < allEdges.length; i++) {
                var e = allEdges[i];
                if (relatedNodes.has(e.from) && relatedNodes.has(e.to)) {
                    updateEdges.push({id: e.id, color: originalEdges[e.id], hidden: false});
                } else {
                    updateEdges.push({id: e.id, color: "rgba(200,200,200,0.25)"});
                }
            }

        } else {
            // Clic dans le vide : on remet tout à la normale
            for (var i = 0; i < allNodes.length; i++) {
                var n = allNodes[i];
                updateNodes.push({
                    id: n.id, 
                    color: originalNodes[n.id].color,
                    font: {color: originalNodes[n.id].fontColor}
                });
            }
            for (var i = 0; i < allEdges.length; i++) {
                updateEdges.push({id: allEdges[i].id, color: originalEdges[allEdges[i].id]});
            }
        }
        
        nodes.update(updateNodes);
        edges.update(updateEdges);
    });

    // 4. Recherche textuelle
    var searchTerm = "%SEARCH%".toLowerCase();

    if (searchTerm.length > 1) {
        var match = allNodes.find(n => 
            n.label && n.label.toLowerCase().includes(searchTerm)
        );

        if (match) {
            network.focus(match.id, { scale: 1.6 });

            nodes.update({
                id: match.id,
                borderWidth: 4,
                color: {
                    border: 'red'
                }
            });
        }
    }
});
</script>
"""

    html = html.replace("%SEARCH%", search.lower())

    # ✅ Injection JS
    html = html.replace("</body>", js + "</body>")

    # ✅ Écriture sécurisée UTF-8
    with open(temp_file.name, "w", encoding="utf-8") as f:
        f.write(html)

    return temp_file.name
