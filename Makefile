# build awesome-blogdown.com
.PHONY : all
all : docs/sites.json logs/json-valid.log

docs/sites.json : json/*.json
	./tools/build-json.sh ./json ./docs/sites.json
	
logs/json-valid.log : docs/sites.json
	-mkdir ./logs
	./tools/abjsonchk.sh ./docs/sites.json >> ./logs/json-valid.log

.PHONY : clean
clean :
	-rm ./logs/* 
	-rm docs/sites.json
