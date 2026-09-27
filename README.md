# Перенос Hermes Agent

Приватный воспроизводимый снимок текущей системы Hermes Agent: MASTER/default и профили `astradocs`, `bitrix24`, `designer`, `developer`, `researcher`, `socialresearcher`.

Профили с локальными моделями намеренно исключены: `ruenterprise` и `ruenterprisedocs`. Builder также автоматически исключает профили с локальным provider/base URL и записывает причину в `manifest.json`.

## Что включено

- `config.yaml`, `profile.yaml`, `SOUL.md`/`PROFILE.md` и управляющие README каждого профиля (секретные поля заменены на `<SET_ON_TARGET>`);
- память, skills, plugins, hooks, cron, assets и UI-расширения;
- полная история разговоров в проверенных SQLite-снимках `state.db.gz`; крупные архивы автоматически делятся на 64-МиБ части и прозрачно собираются при проверке/восстановлении;
- точный Git commit установленного Hermes и patch локальных изменений;
- manifest с SHA-256 для каждого файла;
- проверяемый скрипт восстановления.

## Что намеренно исключено

Живые секреты и машинное состояние: `.env`, `auth.json`, OAuth-токены, ключи API, Telegram bot token, pairing, PID/lock-файлы, логи, кэши, виртуальные окружения и скачанные бинарники. Также не включены пользовательские project workspaces и рабочие документы: они не являются состоянием Hermes и должны переноситься отдельным проектным backup. Их публикация даже в private repository создаёт ненужный риск и оставляет секреты в истории Git.

Файл `.env.restore-example` появится после восстановления и сохранит несекретные параметры/имена обязательных переменных. Секреты необходимо ввести заново на целевом устройстве.

## Восстановление на другом устройстве

1. Установить Git и Python 3.11+.
2. Установить Hermes Agent официальным установщиком:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

3. Клонировать этот приватный репозиторий и проверить снимок:

```bash
gh repo clone b0tgptacc/hermes-agent-backup
cd hermes-agent-backup
python verify_snapshot.py
```

4. Остановить gateway и восстановить данные и точную версию исходников:

```bash
hermes gateway stop
python restore.py --force --restore-source
```

Если используется нестандартный каталог, передать `--target PATH` или задать `HERMES_HOME`.
Абсолютные пути исходного `HERMES_HOME` и домашнего каталога пользователя в `config.yaml` автоматически переписываются под целевое устройство.

5. Настроить авторизацию локально, не коммитя секреты:

```bash
hermes setup
hermes auth
```

Для Telegram потребуется заново указать bot token в локальном `.env`; несекретные идентификаторы сохранены в `.env.restore-example`.
Machine-local зависимости профилей (браузеры, OCR-модели, MCP `node_modules`, venv) устанавливаются заново на целевом устройстве; их пути будут видны в восстановленном `config.yaml` и profile README.

6. Проверить и запустить:

```bash
hermes doctor
hermes config check
hermes gateway start
hermes status --all
```

## Обновление снимка с исходного устройства

```bash
python tools/build_snapshot.py --hermes-home "$HERMES_HOME" --output . \
  --exclude-profile ruenterprise --exclude-profile ruenterprisedocs
python verify_snapshot.py
git add -A
git commit -m "Update Hermes snapshot"
git push
```

Скрипт сборки никогда не копирует `.env` или `auth.json`; он создаёт только санитизированный `.env.example`.

## Версия и целостность

Точная версия, commit, локальный source patch, профили, размеры и SHA-256 записаны в `manifest.json`. Перед восстановлением `restore.py` повторно проверяет все хэши, а после распаковки каждой базы выполняет `PRAGMA integrity_check`.
