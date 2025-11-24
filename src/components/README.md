# Components

This folder is the components needed to capture the face from the UI. Controlled by the facialController.

## Flowchart Visualization

```mermaid
---
title: Facial Sequence
---
flowchart LR
    Capture["1. Capture"]
    Comparison["2. Comparison"]
    Recognition["3. Recognition"]

    Capture --> Comparison --> Recognition;
```

## Future Considerations

While it runs fine now, theres a lot of redunancy that could be cut. Additionally, we could benefit from more functions in the facial controller to utilize different functions.

## Components Breakdown

```mermaid
---
title: Capture
---
classDiagram
    Capture
    Capture: +String img_path
    Capture: +capture_entry()
    Capture: +capture_entry()

```

### Comparison

```mermaid
---
title: Comparison
---
classDiagram
    Recognition
    Recognition: +Array known_faces
    Recognition: +Array known_faces
    Recognition: +load_known_faces()


```