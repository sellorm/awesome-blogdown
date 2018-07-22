# build and run the container
.PHONY : all
all : build.trigger ab200-run.log

docker-build.log : Dockerfile ab200.py Makefile
	docker build -t ab200:latest . > docker-build.log

build.trigger :
	touch build.trigger

ab200-run.log : Makefile ab200.py Dockerfile docker-build.log build.trigger
	docker run -e SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL} -e BLOGDOWN_JSON_URL=${BLOGDOWN_JSON_URL} ab200:latest > ab200-run.log

.PHONY : clean
clean :
	-rm *.log
