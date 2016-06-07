from javax.swing import JMenu, JMenuItem


class Menu(JMenu):

    def __init__(self, menuView, name, keyEvent, menuItems, separators):
        self.menuView = menuView
        self.setText(name)
        self.setMnemonic(keyEvent)
        self.items = self.createItems(menuItems)
        for item in self.items:
            self.add(item)
            if item.getText() in separators:
                self.addSeparator()

    def createItems(self, menuItems):
        items = []

        # Refer to MenuView's menuItems dictionary where each menu item has an
        # array of two elements, the first is the key event and the second is
        # the action asigned to the menu item
        def getMethod(name):
            return menuItems[name][1]

        def getKeyEvent(name):
            return menuItems[name][0]

        for name, keyEvent in menuItems.items():
            actionPerformed = getattr(self.menuView.controller, getMethod(name))
            item = JMenuItem(name, actionPerformed=actionPerformed)
            item.setMnemonic(getKeyEvent(name))
            items.append(item)

        return items
