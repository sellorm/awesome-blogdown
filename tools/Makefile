# build and run the container
.PHONY : all
all : ab200-run.log

docker-build.log : Dockerfile ab200.py Makefile
	docker build -t ab200:latest . > docker-build.log

ab200-run.log : Makefile ab200.py Dockerfile docker-build.log
	docker run --rm -e SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL} \
	    -e BLOGDOWN_JSON_URL=${BLOGDOWN_JSON_URL} \
	    sellorm/ab200:latest > ab200-run.log

.PHONY : clean
clean :
	-rm ab200-run.log
	
.PHONY : clean-all
clean-all :
	-rm *.log
