# Jenkins job `ZaharKr_toolshop_diploma`

1. New Item → Freestyle → `ZaharKr_toolshop_diploma`
2. Label: `python`
3. Git: `https://github.com/ZaharKr/toolshop_diploma.git`, `*/main`
4. Parameters: `SUITE` (`all` / `api` / `ui`), `BROWSER`, `BROWSER_VERSION`, `WINDOW_SIZE`, `BASE_URL`, `REMOTE_URL`
5. Create Text File → `.env` с Selenoid login/password
6. Execute shell: [`job-shell.sh`](job-shell.sh)
7. Allure Report → `allure-results`
8. Telegram: allure-notifications 4.11.1 + SOCKS `proxy.qaguru.school:7777`

https://jenkins.qa.guru/job/ZaharKr_toolshop_diploma/  
https://jenkins.qa.guru/job/ZaharKr_toolshop_diploma/allure
