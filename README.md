# AwareTeam. АГЕНТ.

Веб-приложение, помогающее исследователям работать с научными статьями.
Разработано командой **AwareTeam** в рамках хакатона [Deephack.Agents](https://agents.deephack.me/)

Стек технологий: 
- backend: python, fast api, gigachain (langchain), gigachat
- frontend: java script, ionic, vue

### [Презентация](./presentation.pdf)

## Usage

### Docker

```bash
git clone https://gitverse.ru/sc/999/DeepHack-Fullstack.git
cat > .env << EOL
GIGACHAT="<ваш токен>"
SCOPE="<ваш scope>"
MODEL="<модель, которую хотите использовать (лучше Pro)>"
EOL
docker compose up
```

### Manual

```bash
git clone https://gitverse.ru/sc/999/DeepHack-Fullstack.git
```

Backend
```bash
cd DeepHack-Backend/
cat > .env << EOL
GIGACHAT="<ваш токен>"
SCOPE="<ваш scope>"
MODEL="<модель, которую хотите использовать (лучше Pro)>"
EOL
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 5000
```

Frontend
```bash
cd DeepHack-Frontend/
npm i
npm run dev
```
