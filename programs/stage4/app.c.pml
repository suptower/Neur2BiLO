---
format:          pml-0.1
triple:          riscv32-unknown-unknown-elf
bitcode-functions:
  - name:            isr1
    level:           bitcode
    hash:            0
    blocks:
      - name:            isr1_entry
        predecessors:    []
        successors:      []
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
            opcode:          ret
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
            opcode:          alloca
          - index:           4
            opcode:          alloca
          - index:           5
            opcode:          alloca
          - index:           6
            opcode:          call
          - index:           7
            opcode:          store
            memmode:         store
          - index:           8
            opcode:          call
          - index:           9
            opcode:          store
            memmode:         store
          - index:           10
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
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
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
          - task1_for.cond9
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond9
        predecessors:
          - task1_for.inc12
          - task1_for.end7
        successors:
          - task1_for.body11
          - task1_for.end14
        loops:
          - task1_for.cond9
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
      - name:            task1_for.body11
        predecessors:
          - task1_for.cond9
        successors:
          - task1_for.inc12
        loops:
          - task1_for.cond9
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
            opcode:          br
      - name:            task1_for.inc12
        predecessors:
          - task1_for.body11
        successors:
          - task1_for.cond9
        loops:
          - task1_for.cond9
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
      - name:            task1_for.end14
        predecessors:
          - task1_for.cond9
        successors:
          - task1_for.cond16.cc_loopbegin
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond16.cc_loopbegin
        predecessors:
          - task1_for.end14
        successors:
          - task1_for.cond16
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.cond16
        predecessors:
          - task1_for.inc19
          - task1_for.cond16.cc_loopbegin
        successors:
          - task1_for.body18
          - task1_for.end21.cc_loopend
        loops:
          - task1_for.cond16
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
      - name:            task1_for.body18
        predecessors:
          - task1_for.cond16
        successors:
          - task1_for.inc19
        loops:
          - task1_for.cond16
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.inc19
        predecessors:
          - task1_for.body18
        successors:
          - task1_for.cond16
        loops:
          - task1_for.cond16
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
      - name:            task1_for.end21.cc_loopend
        predecessors:
          - task1_for.cond16
        successors:
          - task1_for.end21
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.end21
        predecessors:
          - task1_for.end21.cc_loopend
        successors:
          - task1_for.cond23
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond23
        predecessors:
          - task1_for.inc27
          - task1_for.end21
        successors:
          - task1_for.body25
          - task1_for.end29
        loops:
          - task1_for.cond23
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
      - name:            task1_for.body25
        predecessors:
          - task1_for.cond23
        successors:
          - task1_for.inc27
        loops:
          - task1_for.cond23
        instructions:
          - index:           0
            opcode:          load
            memmode:         load
          - index:           1
            opcode:          mul
          - index:           2
            opcode:          load
            memmode:         load
          - index:           3
            opcode:          sub
          - index:           4
            opcode:          store
            memmode:         store
          - index:           5
            opcode:          br
      - name:            task1_for.inc27
        predecessors:
          - task1_for.body25
        successors:
          - task1_for.cond23
        loops:
          - task1_for.cond23
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
      - name:            task1_for.end29
        predecessors:
          - task1_for.cond23
        successors:
          - task1_for.end29.PSplit.1
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
            opcode:          br
      - name:            task1_for.end29.PSplit.1
        predecessors:
          - task1_for.end29
        successors:
          - task1_for.end29.PSplit.0
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.end29.PSplit.0
        predecessors:
          - task1_for.end29.PSplit.1
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
  - scope:
      function:        task1
      loop:            task1_for.cond9
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond9
    op:              less-equal
    rhs:             2501
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
  - scope:
      function:        task1
      loop:            task1_for.cond16
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond16
    op:              less-equal
    rhs:             901
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
  - scope:
      function:        task1
      loop:            task1_for.cond23
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond23
    op:              less-equal
    rhs:             2501
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
...
---
format:          pml-0.1
triple:          riscv32-unknown-unknown-elf
relation-graphs:
  - src:
      function:        isr1
      level:           bitcode
    dst:
      function:        '0'
      level:           machinecode
    nodes:
      - name:            0
        type:            entry
        src-block:       isr1_entry
        dst-block:       0
        src-successors:  [ 1 ]
        dst-successors:  [ 1 ]
      - name:            1
        type:            exit
        src-block:       ''
        dst-block:       0
    status:          valid
  - src:
      function:        task1
      level:           bitcode
    dst:
      function:        '1'
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
        src-successors:  [ 27 ]
        dst-successors:  [ 27 ]
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
        src-successors:  [ 26 ]
        dst-successors:  [ 26 ]
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
        src-block:       task1_for.cond9
        dst-block:       11
        src-successors:  [ 11, 12 ]
        dst-successors:  [ 11, 12 ]
      - name:            11
        type:            progress
        src-block:       task1_for.body11
        dst-block:       12
        src-successors:  [ 25 ]
        dst-successors:  [ 25 ]
      - name:            12
        type:            progress
        src-block:       task1_for.end14
        dst-block:       14
        src-successors:  [ 13 ]
        dst-successors:  [ 13 ]
      - name:            13
        type:            progress
        src-block:       task1_for.cond16.cc_loopbegin
        dst-block:       15
        src-successors:  [ 14 ]
        dst-successors:  [ 14 ]
      - name:            14
        type:            progress
        src-block:       task1_for.cond16
        dst-block:       16
        src-successors:  [ 15, 16 ]
        dst-successors:  [ 15, 16 ]
      - name:            15
        type:            progress
        src-block:       task1_for.body18
        dst-block:       17
        src-successors:  [ 24 ]
        dst-successors:  [ 24 ]
      - name:            16
        type:            progress
        src-block:       task1_for.end21.cc_loopend
        dst-block:       19
        src-successors:  [ 17 ]
        dst-successors:  [ 17 ]
      - name:            17
        type:            progress
        src-block:       task1_for.end21
        dst-block:       20
        src-successors:  [ 18 ]
        dst-successors:  [ 18 ]
      - name:            18
        type:            progress
        src-block:       task1_for.cond23
        dst-block:       21
        src-successors:  [ 19, 20 ]
        dst-successors:  [ 19, 20 ]
      - name:            19
        type:            progress
        src-block:       task1_for.body25
        dst-block:       22
        src-successors:  [ 23 ]
        dst-successors:  [ 23 ]
      - name:            20
        type:            progress
        src-block:       task1_for.end29
        dst-block:       24
        src-successors:  [ 21 ]
        dst-successors:  [ 21 ]
      - name:            21
        type:            progress
        src-block:       task1_for.end29.PSplit.1
        dst-block:       25
        src-successors:  [ 22 ]
        dst-successors:  [ 22 ]
      - name:            22
        type:            progress
        src-block:       task1_for.end29.PSplit.0
        dst-block:       26
        src-successors:  [ 1 ]
        dst-successors:  [ 1 ]
      - name:            23
        type:            progress
        src-block:       task1_for.inc27
        dst-block:       23
        src-successors:  [ 18 ]
        dst-successors:  [ 18 ]
      - name:            24
        type:            progress
        src-block:       task1_for.inc19
        dst-block:       18
        src-successors:  [ 14 ]
        dst-successors:  [ 14 ]
      - name:            25
        type:            progress
        src-block:       task1_for.inc12
        dst-block:       13
        src-successors:  [ 10 ]
        dst-successors:  [ 10 ]
      - name:            26
        type:            progress
        src-block:       task1_for.inc5
        dst-block:       8
        src-successors:  [ 6 ]
        dst-successors:  [ 6 ]
      - name:            27
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
    mapsto:          isr1
    hash:            0
    blocks:
      - name:            0
        mapsto:          isr1_entry
        predecessors:    [  ]
        successors:      [  ]
        src-hint:        'isr1:8'
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
            opcode:          LUI
            size:            4
          - index:           9
            opcode:          LW
            size:            4
            memmode:         load
          - index:           10
            opcode:          ADDI
            size:            4
          - index:           11
            opcode:          SW
            size:            4
            memmode:         store
          - index:           12
            opcode:          LW
            size:            4
            memmode:         load
          - index:           13
            opcode:          LW
            size:            4
            memmode:         load
          - index:           14
            opcode:          ADDI
            size:            4
          - index:           15
            opcode:          PseudoRET
            size:            4
            branch-type:     return
  - name:            '1'
    level:           machinecode
    mapsto:          task1
    hash:            0
    blocks:
      - name:            0
        mapsto:          task1_entry
        predecessors:    [  ]
        successors:      [ 1 ]
        src-hint:        'task1:13'
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
        src-hint:        'task1:17'
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
        src-hint:        'task1:18'
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
        src-hint:        'task1:17'
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
        src-hint:        'task1:23'
        instructions:
          - index:           0
            opcode:          ADDI
            size:            4
          - index:           1
            opcode:          SW
            size:            4
            memmode:         store
          - index:           2
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            5
        mapsto:          task1_for.cond2.cc_loopbegin
        predecessors:    [ 4 ]
        successors:      [ 6 ]
        src-hint:        'task1:23'
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
        src-hint:        'task1:23'
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
        src-hint:        'task1:24'
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
        src-hint:        'task1:23'
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
        src-hint:        'task1:29'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            10
        mapsto:          task1_for.end7
        predecessors:    [ 9 ]
        successors:      [ 11 ]
        src-hint:        'task1:29'
        instructions:
          - index:           0
            opcode:          ADDI
            size:            4
          - index:           1
            opcode:          SW
            size:            4
            memmode:         store
          - index:           2
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            11
        mapsto:          task1_for.cond9
        predecessors:    [ 10, 13 ]
        successors:      [ 12, 14 ]
        loops:           [ 11 ]
        src-hint:        'task1:29'
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
      - name:            12
        mapsto:          task1_for.body11
        predecessors:    [ 11 ]
        successors:      [ 13 ]
        loops:           [ 11 ]
        src-hint:        'task1:30'
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
      - name:            13
        mapsto:          task1_for.inc12
        predecessors:    [ 12 ]
        successors:      [ 11 ]
        loops:           [ 11 ]
        src-hint:        'task1:29'
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
      - name:            14
        mapsto:          task1_for.end14
        predecessors:    [ 11 ]
        successors:      [ 15 ]
        src-hint:        'task1:35'
        instructions:
          - index:           0
            opcode:          ADDI
            size:            4
          - index:           1
            opcode:          SW
            size:            4
            memmode:         store
          - index:           2
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            15
        mapsto:          task1_for.cond16.cc_loopbegin
        predecessors:    [ 14 ]
        successors:      [ 16 ]
        src-hint:        'task1:35'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            16
        mapsto:          task1_for.cond16
        predecessors:    [ 15, 18 ]
        successors:      [ 17, 19 ]
        loops:           [ 16 ]
        src-hint:        'task1:35'
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
      - name:            17
        mapsto:          task1_for.body18
        predecessors:    [ 16 ]
        successors:      [ 18 ]
        loops:           [ 16 ]
        src-hint:        'task1:36'
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
      - name:            18
        mapsto:          task1_for.inc19
        predecessors:    [ 17 ]
        successors:      [ 16 ]
        loops:           [ 16 ]
        src-hint:        'task1:35'
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
      - name:            19
        mapsto:          task1_for.end21.cc_loopend
        predecessors:    [ 16 ]
        successors:      [ 20 ]
        src-hint:        'task1:41'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            20
        mapsto:          task1_for.end21
        predecessors:    [ 19 ]
        successors:      [ 21 ]
        src-hint:        'task1:41'
        instructions:
          - index:           0
            opcode:          ADDI
            size:            4
          - index:           1
            opcode:          SW
            size:            4
            memmode:         store
          - index:           2
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            21
        mapsto:          task1_for.cond23
        predecessors:    [ 20, 23 ]
        successors:      [ 22, 24 ]
        loops:           [ 21 ]
        src-hint:        'task1:41'
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
      - name:            22
        mapsto:          task1_for.body25
        predecessors:    [ 21 ]
        successors:      [ 23 ]
        loops:           [ 21 ]
        src-hint:        'task1:42'
        instructions:
          - index:           0
            opcode:          LW
            size:            4
            memmode:         load
          - index:           1
            opcode:          SLLI
            size:            4
          - index:           2
            opcode:          LW
            size:            4
            memmode:         load
          - index:           3
            opcode:          SUB
            size:            4
          - index:           4
            opcode:          SW
            size:            4
            memmode:         store
          - index:           5
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            23
        mapsto:          task1_for.inc27
        predecessors:    [ 22 ]
        successors:      [ 21 ]
        loops:           [ 21 ]
        src-hint:        'task1:41'
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
      - name:            24
        mapsto:          task1_for.end29
        predecessors:    [ 21 ]
        successors:      [ 25 ]
        src-hint:        'task1:45'
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
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            25
        mapsto:          task1_for.end29.PSplit.1
        predecessors:    [ 24 ]
        successors:      [ 26 ]
        src-hint:        'task1:47'
        instructions:
          - index:           0
            opcode:          PseudoCALL
            size:            8
            branch-type:     call
          - index:           1
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            26
        mapsto:          task1_for.end29.PSplit.0
        predecessors:    [ 25 ]
        successors:      [  ]
        src-hint:        'task1:48'
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
      - { entry-block: isr1_entry, exit-block: isr1_entry, function: isr1, 
          index: 0 }
      - { entry-block: '', exit-block: '', function: '', index: 1 }
      - { entry-block: task1_entry, exit-block: task1_for.end, function: task1, 
          index: 2 }
      - { entry-block: task1_for.body18, exit-block: task1_for.body18, 
          function: task1, index: 3 }
      - { entry-block: task1_for.body4, exit-block: task1_for.body4, function: task1, 
          index: 4 }
      - { entry-block: task1_for.cond16, exit-block: task1_for.cond16, 
          function: task1, index: 5 }
      - { entry-block: task1_for.cond16.cc_loopbegin, exit-block: task1_for.cond16.cc_loopbegin, 
          function: task1, index: 6 }
      - { entry-block: task1_for.cond2, exit-block: task1_for.cond2, function: task1, 
          index: 7 }
      - { entry-block: task1_for.cond2.cc_loopbegin, exit-block: task1_for.cond2.cc_loopbegin, 
          function: task1, index: 8 }
      - { entry-block: task1_for.cond23, exit-block: task1_for.end29.PSplit.1, 
          function: task1, index: 9 }
      - { entry-block: task1_for.end21, exit-block: task1_for.end21, function: task1, 
          index: 10 }
      - { entry-block: task1_for.end21.cc_loopend, exit-block: task1_for.end21.cc_loopend, 
          function: task1, index: 11 }
      - { entry-block: task1_for.end7, exit-block: task1_for.end14, function: task1, 
          index: 12 }
      - { entry-block: task1_for.end7.cc_loopend, exit-block: task1_for.end7.cc_loopend, 
          function: task1, index: 13 }
      - { entry-block: task1_for.inc19, exit-block: task1_for.inc19, function: task1, 
          index: 14 }
      - { entry-block: task1_for.inc5, exit-block: task1_for.inc5, function: task1, 
          index: 15 }
      - { entry-block: '', exit-block: '', function: '', index: 16 }
    devices:
      - { power: 105648000, index: 0, name: CpuHighFreq }
      - { power: 28483000, index: 1, name: CpuLowFreq }
      - { power: 0, index: 2, name: UartOn }
      - { power: 0, index: 3, name: OsDefault }
    entry-nodes:     [ 2 ]
    exit-nodes:      [ 30, 29 ]
    name:            pstg-main
    nodes:
      - pabb:            0
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 15, 36, 48, 51, 54, 62, 67 ]
        predecessor-edges: [ 11, 18, 32, 38, 49, 53, 66 ]
        input-constraint: { inputs: [ 11, 18, 32, 38, 49, 53, 66 ], potential-inputs: [  ] }
        index:           0
      - pabb:            0
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 0, 25, 44, 47, 55, 61, 68, 74 ]
        predecessor-edges: [ 2, 6, 22, 27, 42, 45, 60, 73 ]
        input-constraint: { inputs: [ 2, 6, 22, 27, 42, 45, 60, 73 ], potential-inputs: [  ] }
        index:           1
      - pabb:            1
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 1 ]
        predecessor-edges: [  ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [  ], potential-inputs: [  ] }
        index:           2
      - pabb:            2
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 2, 3, 4 ]
        predecessor-edges: [ 0, 1 ]
        input-constraint: { inputs: [ 1 ], potential-inputs: [  ] }
        index:           3
      - pabb:            3
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 37 ]
        predecessor-edges: [ 33 ]
        costs:           { time_ns: 110000, power_nW: 24832209 }
        input-constraint: { inputs: [ 33 ], potential-inputs: [  ] }
        index:           4
      - pabb:            3
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 56 ]
        predecessor-edges: [ 28 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 28 ], potential-inputs: [  ] }
        index:           5
      - pabb:            4
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 16 ]
        predecessor-edges: [ 12 ]
        costs:           { time_ns: 110000, power_nW: 24832209 }
        input-constraint: { inputs: [ 12 ], potential-inputs: [  ] }
        index:           6
      - pabb:            4
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 69 ]
        predecessor-edges: [ 7 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 7 ], potential-inputs: [  ] }
        index:           7
      - pabb:            5
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 32, 33, 34, 35 ]
        predecessor-edges: [ 17, 31, 36, 52, 64 ]
        input-constraint: { inputs: [ 17, 31, 52, 64 ], potential-inputs: [  ] }
        index:           8
      - pabb:            5
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 26, 27, 28, 29 ]
        predecessor-edges: [ 23, 30, 55, 59, 63 ]
        input-constraint: { inputs: [ 23, 30, 59, 63 ], potential-inputs: [  ] }
        index:           9
      - pabb:            6
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 63, 64 ]
        predecessor-edges: [ 19 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 19 ], potential-inputs: [  ] }
        index:           10
      - pabb:            6
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 30, 31 ]
        predecessor-edges: [ 24 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 24 ], potential-inputs: [  ] }
        index:           11
      - pabb:            7
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 11, 12, 13, 14 ]
        predecessor-edges: [ 10, 15, 65 ]
        input-constraint: { inputs: [ 10, 65 ], potential-inputs: [  ] }
        index:           12
      - pabb:            7
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 5, 6, 7, 8 ]
        predecessor-edges: [ 3, 9, 68, 72 ]
        input-constraint: { inputs: [ 3, 9, 72 ], potential-inputs: [  ] }
        index:           13
      - pabb:            8
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 9, 10 ]
        predecessor-edges: [ 4 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 4 ], potential-inputs: [  ] }
        index:           14
      - pabb:            9
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 49, 50 ]
        predecessor-edges: [ 39, 51 ]
        input-constraint: { inputs: [ 39 ], potential-inputs: [  ] }
        index:           15
      - pabb:            9
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 45, 46 ]
        predecessor-edges: [ 43, 47 ]
        input-constraint: { inputs: [ 43 ], potential-inputs: [  ] }
        index:           16
      - pabb:            10
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 38, 39 ]
        predecessor-edges: [ 34, 40, 48, 57 ]
        input-constraint: { inputs: [ 34, 40, 57 ], potential-inputs: [  ] }
        index:           17
      - pabb:            10
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 42, 43 ]
        predecessor-edges: [ 26, 41, 44, 58 ]
        input-constraint: { inputs: [ 26, 41, 58 ], potential-inputs: [  ] }
        index:           18
      - pabb:            11
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 40, 41 ]
        predecessor-edges: [ 35 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 35 ], potential-inputs: [  ] }
        index:           19
      - pabb:            11
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 57, 58 ]
        predecessor-edges: [ 29 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 29 ], potential-inputs: [  ] }
        index:           20
      - pabb:            12
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 17, 18, 19 ]
        predecessor-edges: [ 13, 20, 62, 70 ]
        input-constraint: { inputs: [ 13, 20, 70 ], potential-inputs: [  ] }
        index:           21
      - pabb:            12
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 22, 23, 24 ]
        predecessor-edges: [ 5, 21, 25, 71 ]
        input-constraint: { inputs: [ 5, 21, 71 ], potential-inputs: [  ] }
        index:           22
      - pabb:            13
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 20, 21 ]
        predecessor-edges: [ 14 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 14 ], potential-inputs: [  ] }
        index:           23
      - pabb:            13
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 70, 71 ]
        predecessor-edges: [ 8 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 8 ], potential-inputs: [  ] }
        index:           24
      - pabb:            14
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 52, 53 ]
        predecessor-edges: [ 37, 54 ]
        input-constraint: { inputs: [ 37 ], potential-inputs: [  ] }
        index:           25
      - pabb:            14
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 59, 60 ]
        predecessor-edges: [ 56, 61 ]
        input-constraint: { inputs: [ 56 ], potential-inputs: [  ] }
        index:           26
      - pabb:            15
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 65, 66 ]
        predecessor-edges: [ 16, 67 ]
        input-constraint: { inputs: [ 16 ], potential-inputs: [  ] }
        index:           27
      - pabb:            15
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 72, 73 ]
        predecessor-edges: [ 69, 74 ]
        input-constraint: { inputs: [ 69 ], potential-inputs: [  ] }
        index:           28
      - pabb:            16
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 50 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 50 ], potential-inputs: [  ] }
        index:           29
      - pabb:            16
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 46 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 46 ], potential-inputs: [  ] }
        index:           30
    edges:
      - index:           0
        source:          1
        target:          3
      - index:           1
        source:          2
        target:          3
      - index:           2
        source:          3
        target:          1
      - index:           3
        source:          3
        target:          13
      - index:           4
        source:          3
        target:          14
      - index:           5
        source:          13
        target:          22
      - index:           6
        source:          13
        target:          1
      - index:           7
        source:          13
        target:          7
      - index:           8
        source:          13
        target:          24
      - index:           9
        source:          14
        target:          13
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           10
        source:          14
        target:          12
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           11
        source:          12
        target:          0
      - index:           12
        source:          12
        target:          6
      - index:           13
        source:          12
        target:          21
      - index:           14
        source:          12
        target:          23
      - index:           15
        source:          0
        target:          12
      - index:           16
        source:          6
        target:          27
      - index:           17
        source:          21
        target:          8
      - index:           18
        source:          21
        target:          0
      - index:           19
        source:          21
        target:          10
      - index:           20
        source:          23
        target:          21
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           21
        source:          23
        target:          22
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           22
        source:          22
        target:          1
      - index:           23
        source:          22
        target:          9
      - index:           24
        source:          22
        target:          11
      - index:           25
        source:          1
        target:          22
      - index:           26
        source:          9
        target:          18
      - index:           27
        source:          9
        target:          1
      - index:           28
        source:          9
        target:          5
      - index:           29
        source:          9
        target:          20
      - index:           30
        source:          11
        target:          9
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           31
        source:          11
        target:          8
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           32
        source:          8
        target:          0
      - index:           33
        source:          8
        target:          4
      - index:           34
        source:          8
        target:          17
      - index:           35
        source:          8
        target:          19
      - index:           36
        source:          0
        target:          8
      - index:           37
        source:          4
        target:          25
      - index:           38
        source:          17
        target:          0
      - index:           39
        source:          17
        target:          15
      - index:           40
        source:          19
        target:          17
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           41
        source:          19
        target:          18
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           42
        source:          18
        target:          1
      - index:           43
        source:          18
        target:          16
      - index:           44
        source:          1
        target:          18
      - index:           45
        source:          16
        target:          1
      - index:           46
        source:          16
        target:          30
      - index:           47
        source:          1
        target:          16
      - index:           48
        source:          0
        target:          17
      - index:           49
        source:          15
        target:          0
      - index:           50
        source:          15
        target:          29
      - index:           51
        source:          0
        target:          15
      - index:           52
        source:          25
        target:          8
      - index:           53
        source:          25
        target:          0
      - index:           54
        source:          0
        target:          25
      - index:           55
        source:          1
        target:          9
      - index:           56
        source:          5
        target:          26
      - index:           57
        source:          20
        target:          17
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           58
        source:          20
        target:          18
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           59
        source:          26
        target:          9
      - index:           60
        source:          26
        target:          1
      - index:           61
        source:          1
        target:          26
      - index:           62
        source:          0
        target:          21
      - index:           63
        source:          10
        target:          9
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           64
        source:          10
        target:          8
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           65
        source:          27
        target:          12
      - index:           66
        source:          27
        target:          0
      - index:           67
        source:          0
        target:          27
      - index:           68
        source:          1
        target:          13
      - index:           69
        source:          7
        target:          28
      - index:           70
        source:          24
        target:          21
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           71
        source:          24
        target:          22
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           72
        source:          28
        target:          13
      - index:           73
        source:          28
        target:          1
      - index:           74
        source:          1
        target:          28
    transition-constraints:
      - { index: 0, left: [ 2 ], right: [ 0 ] }
      - { index: 1, left: [ 11 ], right: [ 15 ] }
      - { index: 2, left: [ 22 ], right: [ 25 ] }
      - { index: 3, left: [ 32 ], right: [ 36 ] }
      - { index: 4, left: [ 42 ], right: [ 44 ] }
      - { index: 5, left: [ 45 ], right: [ 47 ] }
      - { index: 6, left: [ 38 ], right: [ 48 ] }
      - { index: 7, left: [ 49 ], right: [ 51 ] }
      - { index: 8, left: [ 53 ], right: [ 54 ] }
      - { index: 9, left: [ 27 ], right: [ 55 ] }
      - { index: 10, left: [ 60 ], right: [ 61 ] }
      - { index: 11, left: [ 18 ], right: [ 62 ] }
      - { index: 12, left: [ 66 ], right: [ 67 ] }
      - { index: 13, left: [ 6 ], right: [ 68 ] }
      - { index: 14, left: [ 73 ], right: [ 74 ] }
      - { index: 15, left: [ 11 ], right: [ 15 ] }
      - { index: 16, left: [ 32 ], right: [ 36 ] }
      - { index: 17, left: [ 38 ], right: [ 48 ] }
      - { index: 18, left: [ 49 ], right: [ 51 ] }
      - { index: 19, left: [ 53 ], right: [ 54 ] }
      - { index: 20, left: [ 66 ], right: [ 67 ] }
      - { index: 21, left: [ 2 ], right: [ 0 ] }
      - { index: 22, left: [ 22 ], right: [ 25 ] }
      - { index: 23, left: [ 42 ], right: [ 44 ] }
      - { index: 24, left: [ 45 ], right: [ 47 ] }
      - { index: 25, left: [ 60 ], right: [ 61 ] }
      - { index: 26, left: [ 73 ], right: [ 74 ] }
      - { index: 27, left: [ 0, 1 ], right: [ 2, 3, 4 ] }
      - { index: 28, left: [ 33 ], right: [ 37 ] }
      - { index: 29, left: [ 28 ], right: [ 56 ] }
      - { index: 30, left: [ 12 ], right: [ 16 ] }
      - { index: 31, left: [ 7 ], right: [ 69 ] }
      - { index: 32, left: [ 17, 31, 36, 52, 64 ], right: [ 32, 33, 34, 
                                                            35 ] }
      - { index: 33, left: [ 23, 30, 55, 59, 63 ], right: [ 26, 27, 28, 
                                                            29 ] }
      - { index: 34, left: [ 19 ], right: [ 63, 64 ] }
      - { index: 35, left: [ 24 ], right: [ 30, 31 ] }
      - { index: 36, left: [ 10, 15, 65 ], right: [ 11, 12, 13, 14 ] }
      - { index: 37, left: [ 3, 9, 68, 72 ], right: [ 5, 6, 7, 8 ] }
      - { index: 38, left: [ 4 ], right: [ 9, 10 ] }
      - { index: 39, left: [ 39, 51 ], right: [ 49, 50 ] }
      - { index: 40, left: [ 43, 47 ], right: [ 45, 46 ] }
      - { index: 41, left: [ 34, 40, 48, 57 ], right: [ 38, 39 ] }
      - { index: 42, left: [ 26, 41, 44, 58 ], right: [ 42, 43 ] }
      - { index: 43, left: [ 35 ], right: [ 40, 41 ] }
      - { index: 44, left: [ 29 ], right: [ 57, 58 ] }
      - { index: 45, left: [ 13, 20, 62, 70 ], right: [ 17, 18, 19 ] }
      - { index: 46, left: [ 5, 21, 25, 71 ], right: [ 22, 23, 24 ] }
      - { index: 47, left: [ 14 ], right: [ 20, 21 ] }
      - { index: 48, left: [ 8 ], right: [ 70, 71 ] }
      - { index: 49, left: [ 37, 54 ], right: [ 52, 53 ] }
      - { index: 50, left: [ 56, 61 ], right: [ 59, 60 ] }
      - { index: 51, left: [ 16, 67 ], right: [ 65, 66 ] }
      - { index: 52, left: [ 69, 74 ], right: [ 72, 73 ] }
    loop-constraints:
      - { index: 0, backlink: [ 0 ], entry: [ 1 ] }
      - { index: 1, backlink: [ 15 ], entry: [ 10, 65 ] }
      - { index: 2, backlink: [ 25 ], entry: [ 5, 21, 71 ] }
      - { index: 3, backlink: [ 36 ], entry: [ 17, 31, 52, 64 ] }
      - { index: 4, backlink: [ 44 ], entry: [ 26, 41, 58 ] }
      - { index: 5, backlink: [ 47 ], entry: [ 43 ] }
      - { index: 6, backlink: [ 48 ], entry: [ 34, 40, 57 ] }
      - { index: 7, backlink: [ 51 ], entry: [ 39 ] }
      - { index: 8, backlink: [ 54 ], entry: [ 37 ] }
      - { index: 9, backlink: [ 55 ], entry: [ 23, 30, 59, 63 ] }
      - { index: 10, backlink: [ 61 ], entry: [ 56 ] }
      - { index: 11, backlink: [ 62 ], entry: [ 13, 20, 70 ] }
      - { index: 12, backlink: [ 67 ], entry: [ 16 ] }
      - { index: 13, backlink: [ 68 ], entry: [ 3, 9, 72 ] }
      - { index: 14, backlink: [ 74 ], entry: [ 69 ] }
      - { index: 15, backlink: [ 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 
                                 32, 33, 34, 35, 36, 37, 38, 39, 40, 48, 
                                 49, 50, 51, 52, 53, 54, 62, 64, 65, 66, 
                                 67 ], entry: [ 10, 31, 57, 70 ] }
      - { index: 16, backlink: [ 59 ], entry: [ 23, 30, 63 ] }
      - { index: 17, backlink: [ 52 ], entry: [ 17, 31, 64 ] }
      - { index: 18, backlink: [ 72 ], entry: [ 3, 9 ] }
      - { index: 19, backlink: [ 65 ], entry: [ 10 ] }
    iat-constraints:
      - { index: 0, entry: [ 2, 6, 11, 18, 22, 27, 32, 38, 42, 45, 49, 
                             53, 60, 66, 73 ], iat: 365000000 }
    upper-bound-constraints:
      - { index: 0, upper-bound: 900, backlink-edges: [ 59, 52 ], entry-edges: [ 
                                                                                 23, 
                                                                                 30, 
                                                                                 63, 
                                                                                 17, 
                                                                                 31, 
                                                                                 64 ] }
      - { index: 1, upper-bound: 900, backlink-edges: [ 72, 65 ], entry-edges: [ 
                                                                                 3, 
                                                                                 9, 
                                                                                 10 ] }
    cc-alternatives:
      - cc-nodes:        [ 11, 10 ]
        alternatives:
          - { edges: [ 17, 23 ] }
          - { edges: [ 30, 63 ] }
          - { edges: [ 31, 64 ] }
      - cc-nodes:        [ 14 ]
        alternatives:
          - { edges: [ 3 ] }
          - { edges: [ 9 ] }
          - { edges: [ 10 ] }
      - cc-nodes:        [ 19, 20 ]
        alternatives:
          - { edges: [ 26, 34 ] }
          - { edges: [ 41, 58 ] }
          - { edges: [ 40, 57 ] }
      - cc-nodes:        [ 23, 24 ]
        alternatives:
          - { edges: [ 5, 13 ] }
          - { edges: [ 21, 71 ] }
          - { edges: [ 20, 70 ] }
...
