import sys
import yaml
from ruamel.yaml import YAML
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QComboBox, QScrollArea,
    QGroupBox, QSpinBox, QLayout, QSizePolicy, QGridLayout, QRadioButton
)
from PyQt5.QtCore import Qt


class CustomGridLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.currentRow = 0
        self.currentCol = 0

    def addNext(self, item):
        if isinstance(item, QWidget):
            self.addWidget(item, self.currentRow, self.currentCol)
        elif isinstance(item, QLayout):
            container = QWidget()
            container.setLayout(item)
            self.addWidget(container, self.currentRow, self.currentCol)

        self.currentCol += 1
        if self.currentCol > 1:
            self.currentRow += 1
            self.currentCol = 0


class BaseWidget(QWidget):
    def __init__(self, label_text):
        super().__init__()

        layout = QVBoxLayout()
        self.label = QLabel(label_text)
        self.setLayout(layout)

    def addWidget(self, widget):
        widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.layout().addWidget(self.label)
        self.layout().addWidget(widget)


class LabeledComboBoxWidget(BaseWidget):
    def __init__(self, label_text, items, default_value=None):
        super().__init__(label_text)

        self.combo_box = QComboBox()
        self.combo_box.addItems(items)
        default_index = 0
        for idx, x in enumerate(items):
            if str(x) == str(default_value):
                default_index = idx
                break
        self.combo_box.setCurrentIndex(default_index)
        self.addWidget(self.combo_box)


class LabeledNumericalInputWidget(BaseWidget):
    def __init__(self, label_text, min_value=None, max_value=None, default_value=None):
        super().__init__(label_text)

        self.input_field = QSpinBox()

        if min_value is not None:
            self.input_field.setMinimum(min_value)
        if max_value is not None:
            self.input_field.setMaximum(max_value)
        if default_value is not None:
            self.input_field.setValue(default_value)

        self.addWidget(self.input_field)


class CustomRadioButtonWidget(BaseWidget):
    def __init__(self, label_text, default_value=None):
        super().__init__(label_text)

        self.radio_button = QRadioButton(label_text)
        if str(default_value).lower() == str(label_text).lower():
            self.radio_button.setChecked(True)
        else:
            self.radio_button.setChecked(False)
        self.addWidget(self.radio_button)


class MainWindow(QWidget):
    """Интерфейс деталей магазина
    """
    car_details = {
        "headlight": [
            {
                "class": LabeledComboBoxWidget,
                "kwargs": {
                    "label_text": "Type",
                    "items": ["right", "left"],
                },
            }, {
                "class": LabeledNumericalInputWidget,
                "kwargs": {
                    "label_text": "Quantity",
                    "min_value": 1,
                    "max_value": 255,
                },
            }
        ],
        "door": [
            {
                "class": LabeledComboBoxWidget,
                "kwargs": {
                    "label_text": "Type",
                    "items": ["front", "back"]
                },
            }, {
                "class": LabeledComboBoxWidget,
                "kwargs": {
                    "label_text": "Side",
                    "items": ["right", "left"]
                },
            }, {
                "class": LabeledNumericalInputWidget,
                "kwargs": {
                    "label_text": "Quantity",
                    "min_value": 1,
                    "max_value": 255
                },
            }
        ],
        "engine": [
            {
                "class": CustomRadioButtonWidget,
                "kwargs": {
                    "label_text": "Gas",
                    "default_value": "Gas",
                }
            }, {
                "class": CustomRadioButtonWidget,
                "kwargs": {
                    "label_text": "Diesel",
                }
            }, {
                "class": LabeledComboBoxWidget,
                "kwargs": {
                    "label_text": "Capacity",
                    "items": ["1.4", "1.6", "1.8"]
                }
            }, {
                "class": LabeledComboBoxWidget,
                "kwargs": {
                    "label_text": "Capacity",
                    "items": ["1.2", "1.4", "1.6"]
                }
            }, {
                "class": LabeledNumericalInputWidget,
                "kwargs": {
                    "label_text": "Quantity",
                    "min_value": 1,
                    "max_value": 255
                },
            }
        ]
    }

    def __init__(self):
        super().__init__()
        self.right_menu = None
        self.left_menu = None
        self.initUI()

    def init_left_menu(self):
        self.left_menu.setFixedWidth(200)
        left_layout = QVBoxLayout(self.left_menu)
        left_layout.setAlignment(Qt.AlignTop)

        # Горизонтальный макет "Сохранить" и "Загрузить"
        buttons_layout = QHBoxLayout()
        button_load = QPushButton('Open', self)
        button_save = QPushButton('Save', self)
        buttons_layout.addWidget(button_load)
        buttons_layout.addWidget(button_save)

        # Выпадающий список магазина
        combo_box = QComboBox(self)
        combo_box.addItems(['headlight', 'door', 'engine'])
        button_add = QPushButton('Add', self)
        self.left_menu.combo_box = combo_box

        # Закрепляем к левому меню
        left_layout.addLayout(buttons_layout)
        left_layout.addWidget(combo_box)
        left_layout.addWidget(button_add)

        # Основные обработчики событий
        button_save.clicked.connect(self.save_action)
        button_load.clicked.connect(self.load_action)
        button_add.clicked.connect(self.add_action)

    def init_right_menu(self):
        right_layout = QVBoxLayout(self.right_menu)
        right_layout.setAlignment(Qt.AlignTop)
        self.right_menu.setMinimumWidth(400)

        # Виджет со скроллом
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setAlignment(Qt.AlignTop)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)
        right_layout.addWidget(scroll_area)

        self.right_menu.scroll_layout = scroll_layout

    def initUI(self):
        main_layout = QHBoxLayout(self)
        self.left_menu = QWidget(self)
        self.right_menu = QWidget(self)

        main_layout.addWidget(self.left_menu)
        main_layout.addWidget(self.right_menu)
        self.setLayout(main_layout)

        self.init_left_menu()
        self.init_right_menu()

        self.setWindowTitle('Свободная касса')
        self.setGeometry(100, 100, 800, 600)

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def save_action(self):
        order_data = []
        for index in range(self.right_menu.scroll_layout.count()):
            container = self.right_menu.scroll_layout.itemAt(index).widget()
            if isinstance(container, QGroupBox):
                item_label = container.findChild(QLabel)
                if item_label:
                    item = item_label.text().split()[0].lower()
                    details = {}
                    for widget in container.findChildren(QWidget):
                        if isinstance(widget, LabeledComboBoxWidget):
                            details[widget.label.text().lower()] = widget.combo_box.currentText()
                        elif isinstance(widget, LabeledNumericalInputWidget):
                            details["qty"] = widget.input_field.value()
                        elif isinstance(widget, CustomRadioButtonWidget):
                            if widget.radio_button.isChecked():
                                details["type"] = widget.label.text().lower()
                    order_data.append({"item": item, **details})

        yml = YAML()
        yml.indent(sequence=4, offset=2)
        with open("order.yml", "w") as file:
            yml.dump({"order": order_data}, file)

    def load_action(self):
        with open("order.yml", "r") as file:
            order = yaml.safe_load(file)["order"]
        self.clear_layout(self.right_menu.scroll_layout)
        for item in order:
            defaults = []
            for key, value in item.items():
                defaults.append(value)
            defaults.pop(0)

            if {"gas"} & set(defaults):
                defaults.insert(defaults.index("gas") + 1, "gas")
                defaults.insert(defaults.index("gas") + 2, defaults[-2])
            elif {"diesel"} & set(defaults):
                defaults.insert(defaults.index("diesel") + 1, "diesel")
                defaults.insert(defaults.index("diesel") + 2, defaults[-2])

            container = self.init_widget_by_class(item["item"], defaults=defaults)
            self.right_menu.scroll_layout.addWidget(container)

    def add_action(self):
        selected_item = self.left_menu.combo_box.currentText()
        self.right_menu.scroll_layout.addWidget(
            self.init_widget_by_class(selected_item)
        )

    def init_widget_by_class(self, selected_item, defaults=None):
        if defaults is None:
            defaults = []
        container = QGroupBox()
        container_layout = CustomGridLayout(container)

        label = QLabel(selected_item.capitalize())
        delete_button = QPushButton("Remove")
        delete_button.clicked.connect(lambda: self.remove_container(container))
        container_layout.addNext(label)
        container_layout.addNext(delete_button)

        for idx, widget_detail in enumerate(self.car_details[selected_item]):
            widget_class = widget_detail["class"]
            kwargs = widget_detail["kwargs"]
            kwargs["default_value"] = defaults[idx]
            widget = widget_class(**kwargs)
            container_layout.addNext(widget)

        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return container

    def remove_container(self, container):
        self.right_menu.scroll_layout.removeWidget(container)
        container.deleteLater()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
