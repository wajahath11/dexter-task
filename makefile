upbuild: build up

up:
	docker-compose -f local.yml up

build:
	docker-compose -f local.yml build

run:
	docker-compose -f local.yml run $(filter-out $@,$(MAKECMDGOALS))

restart:
	docker-compose -f local.yml restart $(filter-out $@,$(MAKECMDGOALS))


down:
	docker-compose -f local.yml down $(filter-out $@,$(MAKECMDGOALS))

destroy:
	docker-compose -f local.yml down -v
