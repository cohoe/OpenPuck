#!/bin/bash

java -Djava.library.path=~/Software/DynamoDBLocal/DynamoDBLocal_lib -jar ~/Software/DynamoDBLocal/DynamoDBLocal.jar -sharedDb -dbPath .
