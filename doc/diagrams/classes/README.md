Diagrams created with pyreverse:

```
pyreverse -o png -p pyoracc python/pyoracc/
pyreverse -o png -p controller python/nammu/controller/
pyreverse -o png -p toolbar python/nammu/view/ToolbarView.py
pyreverse -o png -p menu python/nammu/view/MenuView.py
pyreverse -o png -p model python/nammu/view/ModelView.py
pyreverse -o png -p console python/nammu/view/ConsoleView.py
pyreverse -o png -p atf python/nammu/view/AtfAreaView.py

```

Note it doesn't work for all View Classes. It also doesn't draw relationships between them. 
