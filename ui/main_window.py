# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QMessageBox, QHBoxLayout,
    QGroupBox, QFormLayout, QLabel, QComboBox, QCompleter
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl, QTimer, Signal, Qt
import urllib.parse

from utils.path_manager import get_data_path
from data.loader import load_excel
from data.processor import normalize_columns, clean_data, filter_data
from visualization.mindmap import generate_mindmap


class CustomWebEnginePage(QWebEnginePage):
    """
    Page Web personnalisée pour intercepter les événements de clic
    depuis le graphique pyvis (JavaScript) vers Python.
    """
    node_clicked = Signal(str)

    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if url.scheme() == "pyvis":
            query = url.query()
            if query.startswith("node="):
                node_id = urllib.parse.unquote(query[5:])
                self.node_clicked.emit(node_id)
            return False
        return super().acceptNavigationRequest(url, _type, isMainFrame)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Carte mentale interactive")
        self.resize(1300, 800)

        self.df = None

        # --- UI Elements ---
        self.combo_organe = QComboBox()
        self.combo_organe.addItem("Tous les organes")

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher...")

        self.reset_button = QPushButton("Réinitialiser")
        
        self.web_view = QWebEngineView()
        self.custom_page = CustomWebEnginePage(self.web_view)
        self.web_view.setPage(self.custom_page)
        self.custom_page.node_clicked.connect(self.on_node_clicked)

        # Panneau détail
        self.detail_box = QGroupBox("Détails")
        form_layout = QFormLayout()

        self.label_organe = QLabel("-")
        self.label_type = QLabel("-")
        self.label_inter = QLabel("-")
        self.label_def = QLabel("-")
        self.label_code = QLabel("-")

        self.label_def.setWordWrap(True)

        form_layout.addRow("Organe :", self.label_organe)
        form_layout.addRow("Type :", self.label_type)
        form_layout.addRow("Intermédiaire :", self.label_inter)
        form_layout.addRow("Définition :", self.label_def)
        form_layout.addRow("Code :", self.label_code)

        self.detail_box.setLayout(form_layout)

        # --- Layouts ---
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.combo_organe)
        left_layout.addWidget(self.search_bar)
        left_layout.addWidget(self.reset_button)
        left_layout.addWidget(self.web_view)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, 3)
        main_layout.addWidget(self.detail_box, 1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # --- Styling (QSS) ---
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin-top: 15px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #495057;
            }
            QLineEdit, QComboBox {
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: white;
                color: black;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #339af0;
                selection-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #339af0;
            }
            QPushButton {
                background-color: #339af0;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #228be6;
            }
            QPushButton:pressed {
                background-color: #1c7ed6;
            }
            QLabel {
                font-size: 14px;
                color: #212529;
            }
        """)

        # --- Timers & Events ---
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.setInterval(400) # Debouncing 400ms
        self.search_timer.timeout.connect(self.update_graph)

        self.combo_organe.currentIndexChanged.connect(self.update_graph)
        self.search_bar.textChanged.connect(self.search_timer.start)
        self.reset_button.clicked.connect(self.reset_search)

        # Chargement
        self.load_data()

    def load_data(self):
        try:
            path = get_data_path()
            df = load_excel(path)
            df = normalize_columns(df)
            df = clean_data(df)

            self.df = df
            
            # Peupler le menu déroulant avec les organes uniques
            organes = sorted(self.df["organe"].dropna().unique().tolist())
            self.combo_organe.blockSignals(True)
            self.combo_organe.clear()
            self.combo_organe.addItem("Tous les organes")
            self.combo_organe.addItems(organes)
            self.combo_organe.blockSignals(False)

            # --- Autocomplétion (Recherche avancée) ---
            all_terms = set()
            for col in self.df.columns:
                all_terms.update(self.df[col].dropna().astype(str).unique())
            
            suggestion_list = sorted([str(t).strip() for t in all_terms if str(t).strip()])
            
            self.completer = QCompleter(suggestion_list, self)
            self.completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.completer.setFilterMode(Qt.MatchContains)
            
            # Styling du pop-up de complétion pour qu'il soit bien lisible (noir sur blanc)
            self.completer.popup().setStyleSheet("""
                QListView {
                    background-color: white;
                    color: black;
                    selection-background-color: #339af0;
                    selection-color: white;
                    border: 1px solid #ced4da;
                }
            """)
            
            self.search_bar.setCompleter(self.completer)

            self.update_graph()

        except Exception as e:
            self.show_error(str(e))

    def update_graph(self):
        try:
            if self.df is None:
                return

            search = self.search_bar.text()
            organe_sel = self.combo_organe.currentText()
            if organe_sel == "Tous les organes":
                organe_sel = "Tous"

            df_filtered = filter_data(self.df, search, organe_sel)

            if df_filtered.empty:
                self.web_view.setHtml("<h3 style='font-family:sans-serif; text-align:center; color:#868e96; margin-top:50px;'>Aucun résultat</h3>")
                self.update_details(df_filtered)
                return

            html_path = generate_mindmap(df_filtered, search)
            self.web_view.load(QUrl.fromLocalFile(html_path))

            # On met à jour les détails uniquement si c'est la première recherche et qu'on ne clique pas
            self.update_details(df_filtered)

        except Exception as e:
            self.show_error(str(e))

    def on_node_clicked(self, node_id):
        """
        Appelé quand un nœud est cliqué dans la carte mentale.
        """
        if self.df is None or self.df.empty:
            return

        organe_sel = self.combo_organe.currentText()
        if organe_sel == "Tous les organes":
            organe_sel = "Tous"

        # On recherche dans le scope de l'organe sélectionné
        df_context = filter_data(self.df, "", organe_sel)
        
        # Chercher la première ligne contenant la valeur du nœud exactement
        mask = df_context.apply(lambda row: node_id in row.values.astype(str), axis=1)
        df_match = df_context[mask]

        if not df_match.empty:
            self.update_details(df_match)

    def update_details(self, df):
        if df.empty:
            self.label_organe.setText("-")
            self.label_type.setText("-")
            self.label_inter.setText("-")
            self.label_def.setText("-")
            self.label_code.setText("-")
            return

        row = df.iloc[0]

        self.label_organe.setText(str(row["organe"]))
        self.label_type.setText(str(row["type_atteinte"]))
        self.label_inter.setText(str(row["intermediaire"]))
        self.label_def.setText(str(row["definition"]))
        self.label_code.setText(str(row["code"]))

    def reset_search(self):
        self.combo_organe.setCurrentIndex(0)
        self.search_bar.clear()
        self.update_graph()

    def show_error(self, msg):
        QMessageBox.critical(self, "Erreur", msg)
