# Pulla Vibes Only

**Course**: AT00BY07-3013 Ohjelmistotuotanto ja arkkitehtuuri

## Team members

- Kaisa Juhola
- Teemu Martikainen
- Hans Salosensaari
- Elina Tienhaara

## Homework

0. Team members and git link
1. Vision: [Press release](./docs/pressRelease.md)
2. [Stakeholder Mapping](./docs/02_stakeHolders.md)  
3. Requirements:  
   3a. [Product Requirements](./docs/03_Requirements.md)  
   3b. [Prototype Scope](./docs/03_Prototype_Scope.md)  
4. Architecture: [Domain Model](./docs/04_Domain_Model.md)
5. Demo:  
   5a. [Demo Documentation](./docs/05_Demo_Documentation.md)  
   5b. [Demo Video](https://www.youtube.com/watch?v=NOsp9kxdg4U&t=1s)

## Project Structure

```
.
├── docs/
│   └── 01_pressRelease             # Home work 1: Press Release From the Future
│   └── 02_stakeHolders             # Home work 2: Identifying Stakeholders and their power and impact
│   └── 03_Requirements             # Home work 3a: Listing of product requirements
│   └── 03_Product Scope            # Home work 3b: Prototype Description
│   └── 04_Domain_Model             # Home work 4: Domain Model
│   └── 05_Demo_Documentation       # Home work 5: Project presentation & documentation
├── src/
│   └── lightHeadApp.py             # Main application logic
│   └── rooms.py                    # Room model + lighting settings
│   └── translations.py             # Multilingual support
│   └── ui.py                       # CLI UI utilities
│   └── userhandler.py              # User model + authentication
├── tests/
│   └── test_lightHeadApp.py
│   └── test_rooms.py
│   └── test_translations.py
│   └── test_userhandler.py
└── README.md
```

## Tests

The project uses [pytest](https://pytest.org) for testing. The tests are located in the `tests/` folder and are organized by source file.

### Structure

| Test file | Source file | What is tested |
|---|---|---|
| `test_rooms.py` | `rooms.py` | LightingSettings, Room construction, brightness, color, occupancy, lights on/off, Rooms collection |
| `test_userhandler.py` | `userhandler.py` | User field storage, authentication, invalid credentials, user overwriting |
| `test_translations.py` | `translations.py` | English, Finnish and Swedish translations, fallback behavior, key parity across languages |
| `test_lightHeadApp.py` | `lightHeadApp.py` | App initialization, occupancy toggle flow, lighting presets, staff access, language switching |

### Requirements

Install pytest before running the tests:
`pip install pytest`

### Running the tests

Run all tests from the project root:
`python -m pytest tests/ -v`

Run a single test file:
`python -m pytest tests/test_rooms.py -v`