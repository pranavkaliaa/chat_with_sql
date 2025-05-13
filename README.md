# Chat with Your SQL Databases! 💬 💾

This project allows you to interact with your **Microsoft SQL Server** and **SQLite** databases using natural language. Powered by the awesome **Langchain** framework and the super-fast **Groq API**, you can ask questions in plain English and get answers directly from your data!

## What's Inside? 🛠️

* `app.py`: The main Python application file that handles the natural language processing, database connections, and query execution.

## How Does It Work? 🤔

Under the hood, this project uses:

* **Langchain:** To build the language model application and manage the flow of information between the user, the language model, and the databases.
* **Groq API (with Llama3-8b-8192):** To understand your natural language questions and translate them into SQL queries. Groq's speed makes the interactions nice and snappy!
* **SQLAlchemy:** To provide a clean and efficient way to communicate with both Microsoft SQL Server and SQLite databases.
* **pyodbc:** For connecting to Microsoft SQL Server.
* **sqlite3:** Python's built-in library for working with SQLite databases.

## Getting Started 🚀

Here's how you can get this project up and running:

1.  **Install the required libraries:**

    ```bash
    pip install langchain sqlalchemy pyodbc
    # You might need to install the specific driver for your SQL Server
    # For example, for SQL Server on Linux/macOS:
    # pip install pyodbc
    # On Windows, you might need to ensure the Microsoft ODBC Driver for SQL Server is installed.
    ```

2.  **Set up your Groq API key:**

    * Make sure you have an account with Groq and obtain your API key.
    * You'll likely need to set this as an environment variable or directly in your `app.py` file (be cautious about hardcoding!). For example:

        ```bash
        export GROQ_API_KEY="YOUR_GROQ_API_KEY"
        ```

        or within your Python code (if you choose this method):

        ```python
        groq_api_key = "YOUR_GROQ_API_KEY" # Not recommended for production
        ```

3.  **Configure your database connections in `app.py`:**

    * You'll need to modify the connection strings in `app.py` to point to your Microsoft SQL Server and SQLite databases. This typically involves specifying the server name, database name, username, password (for SQL Server), and the file path (for SQLite).

4.  **Run the application:**

    ```bash
    python app.py
    ```

    Follow the prompts in the application to start chatting with your databases!

## Usage 💡

Once the application is running, you should be able to type natural language questions related to the data in your connected databases. The application will then:

1.  Use Langchain and the Groq API to understand your question and generate the appropriate SQL query.
2.  Execute the SQL query against the specified database.
3.  Present the results back to you in a readable format.

**Example Questions:**

* "What are the names of all customers?" (if you have a 'customers' table)
* "Show me the top 5 products by sales." (if you have 'products' and 'sales' tables)
* "How many orders were placed last month?" (if you have an 'orders' table with a date field)

## Contributing ✨

Contributions are welcome! If you have ideas for improvements, bug fixes, or new features, feel free to open an issue or submit a pull request.

## License 📄

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements 🙏

* The amazing **Langchain** library for providing the core framework.
* The incredibly fast **Groq API** for powering the natural language understanding.
* The **SQLAlchemy** project for the robust database toolkit.
* The developers of **pyodbc** for enabling SQL Server connectivity in Python.
* The Python community for the excellent `sqlite3` module.
