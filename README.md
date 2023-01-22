Project 4 (graded) Medical Database within the Practical course DBMS/Goethe University Frankfurt 

Creator of web app: Eduard Kaucher, s0641340@stud.uni-frankfurt.de

Information on this web app and its usage:
- Technology mainly used: Python, SQL, HTML and CSS with the help of Streamlit
- Branch "prod" is used for the demonstration on 1st February 2023
- Web app is hosted on Streamlit Cloud, which accesses the branch "prod" on GitHub
- For the login, the web app uses the service https://www.dashboardauth.com/
- So the web app is accessed through the following domain: https://medbase.dashboardauth.com/home
- The web app remotely accesses a PostgreSQL database (with secrets stored on Streamlit), which runs creator's localhost
- The database is exposed to the Internet with the help of the service https://localxpose.io/ by freeing up a port
- However, the database is not exposed to the Internet 24/7, but rather only when required for demonstration and testing
- If you want to use the web app, please contact the creator in order to expose the database to the Internet.
