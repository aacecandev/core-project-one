mkdir -p ~/.streamlit/

echo "
[server]\n
headless = true\n
enableCORS=false\n
port = $PORT\n
\n
" > ~/.streamlit/config.toml

echo "
url = $URL\n
\n
" > ~/.streamlit/secrets.toml
