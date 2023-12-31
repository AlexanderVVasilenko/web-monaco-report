# F1 Racing Reports Web App

A web application using Flask to generate reports on Formula 1 racing results.

## Features

- **Driver Report:** View a list of Formula 1 drivers and their lap time statistics.
- **Ordering:** Sort the driver list in ascending or descending order.
- **Driver Details:** Get detailed lap time statistics for a specific driver.

## Prerequisites

- Python 3.x
- Flask
- f1_racing_reports
- pytest

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/AlexanderVVasilenko/web-monaco-report.git
    ```

2. Navigate to the project directory:

    ```bash
    cd your-repository
    ```

3. Install dependencies:

    ```bash
    # If needed
    pip install -r requirements.txt
    ```

4. Run the Flask app:

    ```bash
    python src/web.py
    ```

5. Open your web browser and go to [http://127.0.0.1:5000/report/](http://127.0.0.1:5000/report/) to view the driver report.

## Usage

### Driver Report

To view a list of Formula 1 drivers and their lap time statistics:

- [http://127.0.0.1:5000/report/](http://127.0.0.1:5000/report/)

### Sorting

To sort the driver list in ascending or descending order:

- [http://127.0.0.1:5000/report/?order=asc](http://127.0.0.1:5000/report/?order=asc)
- [http://127.0.0.1:5000/report/?order=desc](http://127.0.0.1:5000/report/?order=desc)

### Driver Details

To view detailed lap time statistics for a specific driver (replace `<driver_id>` with the actual driver ID):

- [http://127.0.0.1:5000/report/drivers/?driver_id=<driver_id>](http://127.0.0.1:5000/report/drivers/?driver_id=<driver_id>)

## Tests

Run the tests using:

```bash
python -m pytest tests/
