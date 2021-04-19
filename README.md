# [Порядок запуска сервисов с помощью docker-compose](docker_service.md)

# Назначение и имена контейнеров в docker-compose
**rediscinema** - redis for cache  
**elasticcinema01** - хранилище elastic  
**clientapicinema** - собственно сам модуль FastApi  
**nginxcinema** - nginx который отдает это все во внешний мир  

## Перечень заданий на 5 спринт
0. [00 Ревью в проекте (Оценка 5)](./tasks/00_review.md)
1. [01 SOLID. Elastic Search (Оценка 5)](./tasks/01_SOLID_ES.md)
2. [02 SOLID. Redis (Оценка 5)](./tasks/02_SOLID_redis.md)
3. [03 SOLID. Views (Оценка 8)](./tasks/03_SOLID_views.md)
4. [04 Инфраструктура для функциональных тестов (Оценка 13)](./tasks/04_functional_test_infra.md)
5. [05 Функциональные тесты - film api (Оценка 5)](./tasks/05_functional_test_film.md)
6. [06 Функциональные тесты - person api (Оценка 5)](./tasks/06_functional_test_person.md)
7. [07 Функциональные тесты - genre api (Оценка 5)](./tasks/07_functional_test_genre.md)
8. [08 Функциональные тесты - search api (Оценка 8)](./tasks/08_functional_test_search.md)
9. [09 OpenAPI документация для клиентов сервиса (Оценка 5)](./tasks/09_openapi.md)
10. [10 Exponential backoff (Оценка 8)](./tasks/10_backoff.md)

Как и в прошлом спринте, мы оценили задачи в стори поинтах.

Вы можете разбить эти задачи на более маленькие, например, распределять между участниками команды не большие куски задания, а маленькие подзадачи. В таком случае не забудьте зафиксировать изменения в issues в репозитории.

**От каждого разработчика ожидается выполнение минимум 40% от общего числа стори поинтов в спринте.**
