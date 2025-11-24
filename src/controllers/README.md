# Controllers

## Description

This controller folder is used to connect the Tkinter View, Database, and Facial Recognition components together.

```mermaid
---
title: Relations
---
flowchart TD;
    Database["1. Database"]-->remoteDb["remoteDatabaseController.py"];
    View["2. View"]-->view_controller["view_controller.py"];
    Facial["3. Facial Recognition"]-->facialDb["facialController.py"];
```
## How it works

Similar to a MVC sequence. When running from main.py the view initiates the necessary components and first frame which is the choose_user_panel. It also connects to the database and sends and recieves necessary data depending on the view.