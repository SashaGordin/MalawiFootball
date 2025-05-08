# Malawi Football Visualization

This project visualizes and analyzes match data for the Malawi National Football Team using Python, Pandas, Plotly, and the Preswald workflow framework.

## Features
- Loads and analyzes match data from CSV
- Visualizes match results, scores, and trends over time
- Interactive plots using Plotly
- Modular workflow using Preswald

## Project Structure
- `hello.py`: Main workflow script
- `data/`: Contains the dataset CSV (`Dataset_Malawi_National_Football_Team_Matches.csv`)
- `images/`: Branding assets (logo, favicon)
- `preswald.toml`: Project and app configuration
- `pyproject.toml`: Python dependencies and build config
- `secrets.toml`: Placeholder for secrets (e.g., database passwords)

## Setup
1. **Python Version**: Requires Python 3.8+
2. **Install dependencies**:
   ```bash
   pip install preswald
   ```
   Or use a tool like `pipenv` or `poetry` with the `pyproject.toml`.
3. **Dataset**: Ensure `data/Dataset_Malawi_National_Football_Team_Matches.csv` is present. (A sample is provided.)
4. **Branding**: Logo and favicon are in `images/` and referenced in `preswald.toml`.
5. **Configuration**: Adjust `preswald.toml` and `secrets.toml` as needed for your environment.

## Running the App
The entry point is `hello.py`, orchestrated by Preswald. To run the workflow:

```bash
python hello.py
```

Or, if using Preswald's app runner (if available):

```bash
preswald run
```

## Customization
- **Data**: Replace or update the CSV in `data/` for new analyses.
- **Branding**: Update `images/logo.png` and `images/favicon.ico` for custom branding.
- **Secrets**: Add any required secrets (e.g., database passwords) to `secrets.toml`.

## License
Specify your license here.

---

*Created with [Preswald](https://pypi.org/project/preswald/)*
