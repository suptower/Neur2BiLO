@echo off
docker run --gpus all -it ^
  -v C:\gurobi\gurobi.lic:/root/gurobi.lic ^
  -v C:\Users\Arda\Documents\GitHub\what-rtos\app:/app ^
  neur2bilo-docker