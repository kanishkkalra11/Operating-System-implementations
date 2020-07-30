#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]){
	if (argc == 1){
		printf("wgrep: searchterm [file ...]\n");
		exit(1);
	}
	if (argc == 2){
		char *line = NULL;
		size_t len = 0;
		ssize_t read;
		while ((read = getline(&line, &len, stdin)) != -1){
			if (strstr(line,argv[1])){
				printf("%s",line);
			}
		}
		return 0;
	}
	for(int i=2; i<argc; i++){
		FILE *fp = fopen(argv[i],"r");
		if (fp==NULL){
			printf("wgrep: cannot open file\n");
			exit(1);
		}
		while (!feof(fp)){
			char temp[100000];
			fgets(temp,100000,fp);
			if (strstr(temp,argv[1])){
				printf("%s",temp);
			}
		}
		fclose(fp);
	}
	return 0;
}