# PayU Form Automation

This project automates the process of submitting a Faktura VAT form to PayU using Python. It retrieves user information from a configuration file and sends a POST request with the necessary data.

## Prerequisites

- Python 3.9 or higher
- Pipenv for managing dependencies

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/struk77/payu-form-automation.git
   cd payu-form-automation
   ```

2. **Install dependencies:**

   Use Pipenv to install the required packages:

   ```bash
   pipenv install
   ```

3. **Activate the virtual environment:**

   ```bash
   pipenv shell
   ```

4. **Create a `config.yaml` file:**

   Create a `config.yaml` file in the root directory with your personal information. Example structure:

   ```yaml
   url: https://doladowania.payu.pl/faktura
   users:
     - id: 1
       tin: XXXXXXXXXX
       invoiceFrequency: MONTHLY
       invoiceAddress_name: John Doe
       invoiceAddress_street: Example Street 123
       invoiceAddress_postalCode: 00-000
       invoiceAddress_city: Example City
       invoiceAddress_country: PL
   ```

## Usage

Run the script with the following command:

```bash
python main.py <order_id> <phone> [user_id]
```

- `<order_id>`: The order number.
- `<phone>`: The phone number.
- `[user_id]`: Optional user ID (default is 1).

## Example

```bash
python main.py 1234567890 123456789 1
```

## License

This project is licensed under the MIT License.
