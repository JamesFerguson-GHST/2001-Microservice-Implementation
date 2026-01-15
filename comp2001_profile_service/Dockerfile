# Use official Python 3.9 on Debian Bullseye
FROM python:3.9-bullseye

# Accept Microsoft SQL Server EULA
ENV ACCEPT_EULA=Y

# Install system packages for SQL Server and Python build tools
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    curl gcc g++ gnupg unixodbc unixodbc-dev odbcinst

# Install Microsoft ODBC Driver 17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile \
    && echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

# Set working directory in container
WORKDIR /app

# Copy project files
COPY . .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Clean up apt cache to reduce image size
RUN apt-get -y clean

# Expose Flask port
EXPOSE 8000

# Run the Flask app
CMD ["python", "app.py"]