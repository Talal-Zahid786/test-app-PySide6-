/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls

Item {
    id: root
    width: 1920
    height: 1080

    RangeSlider {
        id: rangeSlider
        x: 739
        y: 708
        width: 377
        height: 110
        second.value: 0.75
        first.value: 0.25
    }
}
