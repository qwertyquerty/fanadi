from fanadi import *

app = QApplication(sys.argv)
qdarktheme.setup_theme(corner_shape="sharp")
qdarktheme.enable_hi_dpi()
global_font = QFont("Consolas", 12) # Specify font family and point size
app.setFont(global_font)

icon = QIcon()
icon.addFile("triforce.png")
app.setWindowIcon(icon)


window = FanadiWindow()
window.show()

sys.exit(app.exec())
