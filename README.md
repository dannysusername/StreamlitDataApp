## Sprint log
     ### Sprint 1
     - Done: venv, requirements.txt, load_data, cleaned data table
     - Hard: conda (base) and venv both active; CSV mixes vehicle and water columns
     - Next: add widgets and charts


 # Biscayne Bay Water Quality Explorer
    Live app: <URL after Step 3.3>
    ## Purpose          - what the app does and who it's for
    ## Dataset          - autonomous vehicle survey, Biscayne Bay FL, 2022-02-04, 942 readings, ~1 s apart
                          - only the sonde columns are kept (vehicle telemetry dropped)
                          - cleaning: stripped column names, built Timestamp, clipped negative chl/algae to 0,
                            turbidity excluded (sensor fault)
    ## How to use       - sidebar: parameter dropdown, time-window slider, raw-data checkbox
    ## Run locally      - git clone ... / python3 -m venv .venv / source .venv/bin/activate /
                          pip install -r requirements.txt / streamlit run app.py
    ## Tech stack       - Streamlit (UI), pandas (data), Plotly (charts)
    ## Agile process    - user stories as GitHub Issues, Projects board, 3 sprints, Definition of Done
    ## Sprint log       - your retros