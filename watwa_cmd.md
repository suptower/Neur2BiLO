# Watwa commands to run
Given problem `watwa_small`

## 1. Initialize directories
```bash
python -m blo.scripts.00_initialize_directories --problem watwa_small
```

## 2. Initialize problem
```bash
python -m blo.scripts.01_initialize_problem --problem watwa_small
```

## 3. Generate data
```bash
python -m blo.scripts.02_generate_data --problem watwa_small --n_procs 4
```

## 4. Train NN
```bash
python -m blo.scripts.03_train_nn --problem watwa_small --model-type inst_encoder
```
