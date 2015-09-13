#!/bin/bash

dynamodb_load -o http://localhost:8000 teams -l ../../dumps/teams.*.dump
