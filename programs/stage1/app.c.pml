---
format:          pml-0.1
triple:          riscv32-unknown-unknown-elf
bitcode-functions:
  - name:            task1
    level:           bitcode
    hash:            0
    blocks:
      - name:            task1_entry
        predecessors:    []
        successors:
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          alloca
          - index:           1
            opcode:          alloca
          - index:           2
            opcode:          alloca
          - index:           3
            opcode:          call
          - index:           4
            opcode:          store
            memmode:         store
          - index:           5
            opcode:          call
          - index:           6
            opcode:          store
            memmode:         store
          - index:           7
            opcode:          br
      - name:            task1_for.cond
        predecessors:
          - task1_for.inc
          - task1_entry
        successors:
          - task1_for.body
          - task1_for.end
        loops:
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          load
            memmode:         load
          - index:           1
            opcode:          icmp
          - index:           2
            opcode:          call
          - index:           3
            opcode:          br
      - name:            task1_for.body
        predecessors:
          - task1_for.cond
        successors:
          - task1_for.inc
        loops:
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          load
            memmode:         load
          - index:           1
            opcode:          mul
          - index:           2
            opcode:          store
            memmode:         store
          - index:           3
            opcode:          br
      - name:            task1_for.inc
        predecessors:
          - task1_for.body
        successors:
          - task1_for.cond
        loops:
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          load
            memmode:         load
          - index:           1
            opcode:          add
          - index:           2
            opcode:          store
            memmode:         store
          - index:           3
            opcode:          br
      - name:            task1_for.end
        predecessors:
          - task1_for.cond
        successors:
          - task1_for.cond2.cc_loopbegin
        instructions:
          - index:           0
            opcode:          load
            memmode:         load
          - index:           1
            opcode:          load
            memmode:         load
          - index:           2
            opcode:          add
          - index:           3
            opcode:          store
            memmode:         store
          - index:           4
            opcode:          call
          - index:           5
            opcode:          store
            memmode:         store
          - index:           6
            opcode:          br
      - name:            task1_for.cond2.cc_loopbegin
        predecessors:
          - task1_for.end
        successors:
          - task1_for.cond2
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.cond2
        predecessors:
          - task1_for.inc5
          - task1_for.cond2.cc_loopbegin
        successors:
          - task1_for.body4
          - task1_for.end7.cc_loopend
        loops:
          - task1_for.cond2
        instructions:
          - index:           0
            opcode:          load
            memmode:         load
          - index:           1
            opcode:          icmp
          - index:           2
            opcode:          call
          - index:           3
            opcode:          br
      - name:            task1_for.body4
        predecessors:
          - task1_for.cond2
        successors:
          - task1_for.inc5
        loops:
          - task1_for.cond2
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.inc5
        predecessors:
          - task1_for.body4
        successors:
          - task1_for.cond2
        loops:
          - task1_for.cond2
        instructions:
          - index:           0
            opcode:          load
            memmode:         load
          - index:           1
            opcode:          add
          - index:           2
            opcode:          store
            memmode:         store
          - index:           3
            opcode:          br
      - name:            task1_for.end7.cc_loopend
        predecessors:
          - task1_for.cond2
        successors:
          - task1_for.end7
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.end7
        predecessors:
          - task1_for.end7.cc_loopend
        successors:
          - task1_for.end7.PSplit.0
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.end7.PSplit.0
        predecessors:
          - task1_for.end7
        successors:      []
        instructions:
          - index:           0
            opcode:          ret
flowfacts:
  - scope:
      function:        task1
      loop:            task1_for.cond
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond
    op:              less-equal
    rhs:             2501
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
  - scope:
      function:        task1
      loop:            task1_for.cond2
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond2
    op:              less-equal
    rhs:             901
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
...
---
format:          pml-0.1
triple:          riscv32-unknown-unknown-elf
relation-graphs:
  - src:
      function:        task1
      level:           bitcode
    dst:
      function:        '0'
      level:           machinecode
    nodes:
      - name:            0
        type:            entry
        src-block:       task1_entry
        dst-block:       0
        src-successors:  [ 2 ]
        dst-successors:  [ 2 ]
      - name:            1
        type:            exit
        src-block:       ''
        dst-block:       0
      - name:            2
        type:            progress
        src-block:       task1_for.cond
        dst-block:       1
        src-successors:  [ 3, 4 ]
        dst-successors:  [ 3, 4 ]
      - name:            3
        type:            progress
        src-block:       task1_for.body
        dst-block:       2
        src-successors:  [ 12 ]
        dst-successors:  [ 12 ]
      - name:            4
        type:            progress
        src-block:       task1_for.end
        dst-block:       4
        src-successors:  [ 5 ]
        dst-successors:  [ 5 ]
      - name:            5
        type:            progress
        src-block:       task1_for.cond2.cc_loopbegin
        dst-block:       5
        src-successors:  [ 6 ]
        dst-successors:  [ 6 ]
      - name:            6
        type:            progress
        src-block:       task1_for.cond2
        dst-block:       6
        src-successors:  [ 7, 8 ]
        dst-successors:  [ 7, 8 ]
      - name:            7
        type:            progress
        src-block:       task1_for.body4
        dst-block:       7
        src-successors:  [ 11 ]
        dst-successors:  [ 11 ]
      - name:            8
        type:            progress
        src-block:       task1_for.end7.cc_loopend
        dst-block:       9
        src-successors:  [ 9 ]
        dst-successors:  [ 9 ]
      - name:            9
        type:            progress
        src-block:       task1_for.end7
        dst-block:       10
        src-successors:  [ 10 ]
        dst-successors:  [ 10 ]
      - name:            10
        type:            progress
        src-block:       task1_for.end7.PSplit.0
        dst-block:       11
        src-successors:  [ 1 ]
        dst-successors:  [ 1 ]
      - name:            11
        type:            progress
        src-block:       task1_for.inc5
        dst-block:       8
        src-successors:  [ 6 ]
        dst-successors:  [ 6 ]
      - name:            12
        type:            progress
        src-block:       task1_for.inc
        dst-block:       3
        src-successors:  [ 2 ]
        dst-successors:  [ 2 ]
    status:          valid
...
---
format:          pml-0.1
triple:          riscv32-unknown-unknown-elf
machine-functions:
  - name:            '0'
    level:           machinecode
    mapsto:          task1
    hash:            0
    blocks:
      - name:            0
        mapsto:          task1_entry
        predecessors:    [  ]
        successors:      [ 1 ]
        src-hint:        'task1:9'
        instructions:
          - index:           0
            opcode:          ADDI
            size:            4
          - index:           2
            opcode:          SW
            size:            4
            memmode:         store
          - index:           3
            opcode:          SW
            size:            4
            memmode:         store
          - index:           6
            opcode:          ADDI
            size:            4
          - index:           8
            opcode:          ADDI
            size:            4
          - index:           9
            opcode:          SW
            size:            4
            memmode:         store
          - index:           10
            opcode:          ADDI
            size:            4
          - index:           11
            opcode:          SW
            size:            4
            memmode:         store
          - index:           12
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            1
        mapsto:          task1_for.cond
        predecessors:    [ 0, 3 ]
        successors:      [ 2, 4 ]
        loops:           [ 1 ]
        src-hint:        'task1:13'
        instructions:
          - index:           0
            opcode:          LW
            size:            4
            memmode:         load
          - index:           1
            opcode:          LUI
            size:            4
          - index:           2
            opcode:          ADDI
            size:            4
          - index:           3
            opcode:          BLT
            size:            4
            branch-type:     conditional
          - index:           4
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            2
        mapsto:          task1_for.body
        predecessors:    [ 1 ]
        successors:      [ 3 ]
        loops:           [ 1 ]
        src-hint:        'task1:14'
        instructions:
          - index:           0
            opcode:          LW
            size:            4
            memmode:         load
          - index:           1
            opcode:          SLLI
            size:            4
          - index:           2
            opcode:          ADD
            size:            4
          - index:           3
            opcode:          SW
            size:            4
            memmode:         store
          - index:           4
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            3
        mapsto:          task1_for.inc
        predecessors:    [ 2 ]
        successors:      [ 1 ]
        loops:           [ 1 ]
        src-hint:        'task1:13'
        instructions:
          - index:           0
            opcode:          LW
            size:            4
            memmode:         load
          - index:           1
            opcode:          ADDI
            size:            4
          - index:           2
            opcode:          SW
            size:            4
            memmode:         store
          - index:           3
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            4
        mapsto:          task1_for.end
        predecessors:    [ 1 ]
        successors:      [ 5 ]
        src-hint:        'task1:16'
        instructions:
          - index:           0
            opcode:          LW
            size:            4
            memmode:         load
          - index:           1
            opcode:          ADD
            size:            4
          - index:           2
            opcode:          SW
            size:            4
            memmode:         store
          - index:           3
            opcode:          ADDI
            size:            4
          - index:           4
            opcode:          SW
            size:            4
            memmode:         store
          - index:           5
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            5
        mapsto:          task1_for.cond2.cc_loopbegin
        predecessors:    [ 4 ]
        successors:      [ 6 ]
        src-hint:        'task1:20'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            6
        mapsto:          task1_for.cond2
        predecessors:    [ 5, 8 ]
        successors:      [ 7, 9 ]
        loops:           [ 6 ]
        src-hint:        'task1:20'
        instructions:
          - index:           0
            opcode:          LW
            size:            4
            memmode:         load
          - index:           1
            opcode:          ADDI
            size:            4
          - index:           2
            opcode:          BLT
            size:            4
            branch-type:     conditional
          - index:           3
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            7
        mapsto:          task1_for.body4
        predecessors:    [ 6 ]
        successors:      [ 8 ]
        loops:           [ 6 ]
        src-hint:        'task1:21'
        instructions:
          - index:           0
            opcode:          ADDI
            size:            4
          - index:           1
            opcode:          PseudoCALL
            size:            8
            branch-type:     call
          - index:           2
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            8
        mapsto:          task1_for.inc5
        predecessors:    [ 7 ]
        successors:      [ 6 ]
        loops:           [ 6 ]
        src-hint:        'task1:20'
        instructions:
          - index:           0
            opcode:          LW
            size:            4
            memmode:         load
          - index:           1
            opcode:          ADDI
            size:            4
          - index:           2
            opcode:          SW
            size:            4
            memmode:         store
          - index:           3
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            9
        mapsto:          task1_for.end7.cc_loopend
        predecessors:    [ 6 ]
        successors:      [ 10 ]
        src-hint:        'task1:25'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            10
        mapsto:          task1_for.end7
        predecessors:    [ 9 ]
        successors:      [ 11 ]
        src-hint:        'task1:25'
        instructions:
          - index:           0
            opcode:          PseudoCALL
            size:            8
            branch-type:     call
          - index:           1
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            11
        mapsto:          task1_for.end7.PSplit.0
        predecessors:    [ 10 ]
        successors:      [  ]
        src-hint:        'task1:26'
        instructions:
          - index:           0
            opcode:          LW
            size:            4
            memmode:         load
          - index:           1
            opcode:          LW
            size:            4
            memmode:         load
          - index:           2
            opcode:          ADDI
            size:            4
          - index:           3
            opcode:          PseudoRET
            size:            4
            branch-type:     return
...
---
format:          pml-0.1
triple:          riscv32-unknown-unknown-elf
pstgs:
  - blocks:
      - { entry-block: '', exit-block: '', function: '', index: 0 }
      - { entry-block: task1_entry, exit-block: task1_for.end, function: task1, 
          index: 1 }
      - { entry-block: task1_for.body4, exit-block: task1_for.body4, function: task1, 
          index: 2 }
      - { entry-block: task1_for.cond2, exit-block: task1_for.cond2, function: task1, 
          index: 3 }
      - { entry-block: task1_for.cond2.cc_loopbegin, exit-block: task1_for.cond2.cc_loopbegin, 
          function: task1, index: 4 }
      - { entry-block: task1_for.end7, exit-block: task1_for.end7, function: task1, 
          index: 5 }
      - { entry-block: task1_for.end7.cc_loopend, exit-block: task1_for.end7.cc_loopend, 
          function: task1, index: 6 }
      - { entry-block: task1_for.inc5, exit-block: task1_for.inc5, function: task1, 
          index: 7 }
      - { entry-block: '', exit-block: '', function: '', index: 8 }
    devices:
      - { power: 105648000, index: 0, name: CpuHighFreq }
      - { power: 28483000, index: 1, name: CpuLowFreq }
      - { power: 0, index: 2, name: UartOn }
      - { power: 0, index: 3, name: OsDefault }
    entry-nodes:     [ 0 ]
    exit-nodes:      [ 14, 13 ]
    name:            pstg-main
    nodes:
      - pabb:            0
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 14 ]
        predecessor-edges: [  ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [  ], potential-inputs: [  ] }
        index:           0
      - pabb:            1
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 0, 1 ]
        predecessor-edges: [ 14 ]
        input-constraint: { inputs: [ 14 ], potential-inputs: [  ] }
        index:           1
      - pabb:            2
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 10 ]
        predecessor-edges: [ 7 ]
        costs:           { time_ns: 110000, power_nW: 24832209 }
        input-constraint: { inputs: [ 7 ], potential-inputs: [  ] }
        index:           2
      - pabb:            2
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 17 ]
        predecessor-edges: [ 3 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 3 ], potential-inputs: [  ] }
        index:           3
      - pabb:            3
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 7, 8, 9 ]
        predecessor-edges: [ 6, 16 ]
        input-constraint: { inputs: [ 6, 16 ], potential-inputs: [  ] }
        index:           4
      - pabb:            3
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 2, 3, 4 ]
        predecessor-edges: [ 0, 5, 20 ]
        input-constraint: { inputs: [ 0, 5, 20 ], potential-inputs: [  ] }
        index:           5
      - pabb:            4
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 5, 6 ]
        predecessor-edges: [ 1 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 1 ], potential-inputs: [  ] }
        index:           6
      - pabb:            5
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 11 ]
        predecessor-edges: [ 8, 12, 18 ]
        input-constraint: { inputs: [ 8, 12, 18 ], potential-inputs: [  ] }
        index:           7
      - pabb:            5
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 15 ]
        predecessor-edges: [ 2, 13, 19 ]
        input-constraint: { inputs: [ 2, 13, 19 ], potential-inputs: [  ] }
        index:           8
      - pabb:            6
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 12, 13 ]
        predecessor-edges: [ 9 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 9 ], potential-inputs: [  ] }
        index:           9
      - pabb:            6
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 18, 19 ]
        predecessor-edges: [ 4 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 4 ], potential-inputs: [  ] }
        index:           10
      - pabb:            7
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 16 ]
        predecessor-edges: [ 10 ]
        input-constraint: { inputs: [ 10 ], potential-inputs: [  ] }
        index:           11
      - pabb:            7
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 20 ]
        predecessor-edges: [ 17 ]
        input-constraint: { inputs: [ 17 ], potential-inputs: [  ] }
        index:           12
      - pabb:            8
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 11 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 11 ], potential-inputs: [  ] }
        index:           13
      - pabb:            8
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 15 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 15 ], potential-inputs: [  ] }
        index:           14
    edges:
      - index:           0
        source:          1
        target:          5
      - index:           1
        source:          1
        target:          6
      - index:           2
        source:          5
        target:          8
      - index:           3
        source:          5
        target:          3
      - index:           4
        source:          5
        target:          10
      - index:           5
        source:          6
        target:          5
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           6
        source:          6
        target:          4
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           7
        source:          4
        target:          2
      - index:           8
        source:          4
        target:          7
      - index:           9
        source:          4
        target:          9
      - index:           10
        source:          2
        target:          11
      - index:           11
        source:          7
        target:          13
      - index:           12
        source:          9
        target:          7
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           13
        source:          9
        target:          8
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           14
        source:          0
        target:          1
      - index:           15
        source:          8
        target:          14
      - index:           16
        source:          11
        target:          4
      - index:           17
        source:          3
        target:          12
      - index:           18
        source:          10
        target:          7
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           19
        source:          10
        target:          8
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           20
        source:          12
        target:          5
    transition-constraints:
      - { index: 0, left: [ 14 ], right: [ 0, 1 ] }
      - { index: 1, left: [ 7 ], right: [ 10 ] }
      - { index: 2, left: [ 3 ], right: [ 17 ] }
      - { index: 3, left: [ 6, 16 ], right: [ 7, 8, 9 ] }
      - { index: 4, left: [ 0, 5, 20 ], right: [ 2, 3, 4 ] }
      - { index: 5, left: [ 1 ], right: [ 5, 6 ] }
      - { index: 6, left: [ 8, 12, 18 ], right: [ 11 ] }
      - { index: 7, left: [ 2, 13, 19 ], right: [ 15 ] }
      - { index: 8, left: [ 9 ], right: [ 12, 13 ] }
      - { index: 9, left: [ 4 ], right: [ 18, 19 ] }
      - { index: 10, left: [ 10 ], right: [ 16 ] }
      - { index: 11, left: [ 17 ], right: [ 20 ] }
    loop-constraints:
      - { index: 0, backlink: [ 7, 8, 9, 10, 11, 12, 16 ], entry: [ 6, 
                                                                    18 ] }
      - { index: 1, backlink: [ 20 ], entry: [ 0, 5 ] }
      - { index: 2, backlink: [ 16 ], entry: [ 6 ] }
    upper-bound-constraints:
      - { index: 0, upper-bound: 900, backlink-edges: [ 20, 16 ], entry-edges: [ 
                                                                                 0, 
                                                                                 5, 
                                                                                 6 ] }
    cc-alternatives:
      - cc-nodes:        [ 6 ]
        alternatives:
          - { edges: [ 0 ] }
          - { edges: [ 5 ] }
          - { edges: [ 6 ] }
      - cc-nodes:        [ 9, 10 ]
        alternatives:
          - { edges: [ 2, 8 ] }
          - { edges: [ 13, 19 ] }
          - { edges: [ 12, 18 ] }
...
