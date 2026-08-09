@echo off
docker run --gpus all -it --shm-size=4g ^
  -v C:\gurobi\gurobi.lic:/root/gurobi.lic ^
  -v C:\Users\Arda\Documents\GitHub\Neur2BiLO:/app ^
  neur2bilo-docker