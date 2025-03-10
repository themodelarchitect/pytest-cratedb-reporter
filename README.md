# pytest-cratedb-reporter

A pytest plugin that writes test results to a CrateDB database.

## Installation

```bash
pip install pytest-cratedb-reporter
```

## Usage
Run pytest with the `cratedb-url` option:

```bash
pytest --cratedb-url="crate://<host>:<port>" your_tests.py
```
 Replace `host` and `port` with your CrateDB server details. For example:

```bash
pytest --cratedb-url=crate://localhost:4200 example/test_example.py
```
 Verify Results:

The plugin will create a table named `test_results` in your CrateDB database (if it doesn't already exist) and populate it with test result data. You can query the table to view the results.

## Configuration
`--cratedb-url`:

- Specifies the CrateDB connection URL.
- Example: `crate://localhost:4200`

## Database Schema
The plugin uses the following schema for the test_results table:

| Column      | Type      | Description                                   |
| ----------- | --------- | ----------------------------------------------|
| `id`        | `SRING`   | Primary key (UUID).                           |
| `nodeid`    | `STRING`  | The test node ID.                             |
| `outcome`   | `STRING`  | The test outcome (e.g., passed, failed).      |
| `message`   | `TEXT`    | The test message (if applicable).             |
| `backtrace` | `TEXT`    | The test backtrace (if applicable).           |
| `duration`  | `INTEGER` | The test duration in milliseconds.            |
| `timestamp` | `DATETIME`| The timestamp of the test execution.          |
| `passed`    | `BOOLEAN` | True if the test passed, False otherwise.     |
| `failed`    | `BOOLEAN` | True if the test failed, False otherwise.     |

## Example queries
```sql
-- Select all test results:
SELECT * FROM test_results;

-- Select failed tests:
SELECT * FROM test_results WHERE failed = true;

-- Select tests with a duration over 1 second:
SELECT * FROM test_results WHERE duration > 1000;
```

## Development
  Clone the repository:

```bash
git clone https://github.com/themodelarchitect/pytest-cratedb-reporter.git
cd pytest-cratedb-reporter
```
  Create a virtual environment:

```python
python -m venv venv
source venv/bin/activate
```
 Install dependencies:

```bash
pip install -e .
pip install -r requirements.txt
```
 Run tests:

```bash
pytest --cratedb-url="crate://<host>:<port>"
```
## Contribute:

Feel free to submit pull requests with improvements or bug fixes.

## License
This project is licensed under the MIT License.