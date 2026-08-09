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
          - task1_for.cond17.cc_loopbegin
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
      - name:            task1_for.cond17.cc_loopbegin
        predecessors:
          - task1_for.end14
        successors:
          - task1_for.cond17
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.cond17
        predecessors:
          - task1_for.inc20
          - task1_for.cond17.cc_loopbegin
        successors:
          - task1_for.body19
          - task1_for.end22.cc_loopend
        loops:
          - task1_for.cond17
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
      - name:            task1_for.body19
        predecessors:
          - task1_for.cond17
        successors:
          - task1_for.inc20
        loops:
          - task1_for.cond17
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.inc20
        predecessors:
          - task1_for.body19
        successors:
          - task1_for.cond17
        loops:
          - task1_for.cond17
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
      - name:            task1_for.end22.cc_loopend
        predecessors:
          - task1_for.cond17
        successors:
          - task1_for.end22
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.end22
        predecessors:
          - task1_for.end22.cc_loopend
        successors:
          - task1_for.cond24.cc_loopbegin
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond24.cc_loopbegin
        predecessors:
          - task1_for.end22
        successors:
          - task1_for.cond24
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.cond24
        predecessors:
          - task1_for.inc27
          - task1_for.cond24.cc_loopbegin
        successors:
          - task1_for.body26
          - task1_for.end29.cc_loopend
        loops:
          - task1_for.cond24
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
      - name:            task1_for.body26
        predecessors:
          - task1_for.cond24
        successors:
          - task1_for.inc27
        loops:
          - task1_for.cond24
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.inc27
        predecessors:
          - task1_for.body26
        successors:
          - task1_for.cond24
        loops:
          - task1_for.cond24
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
      - name:            task1_for.end29.cc_loopend
        predecessors:
          - task1_for.cond24
        successors:
          - task1_for.end29
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.end29
        predecessors:
          - task1_for.end29.cc_loopend
        successors:
          - task1_for.end29.PSplit.0
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.end29.PSplit.0
        predecessors:
          - task1_for.end29
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
      loop:            task1_for.cond17
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond17
    op:              less-equal
    rhs:             901
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
  - scope:
      function:        task1
      loop:            task1_for.cond24
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond24
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
        src-successors:  [ 28 ]
        dst-successors:  [ 28 ]
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
        src-successors:  [ 27 ]
        dst-successors:  [ 27 ]
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
        src-successors:  [ 26 ]
        dst-successors:  [ 26 ]
      - name:            12
        type:            progress
        src-block:       task1_for.end14
        dst-block:       14
        src-successors:  [ 13 ]
        dst-successors:  [ 13 ]
      - name:            13
        type:            progress
        src-block:       task1_for.cond17.cc_loopbegin
        dst-block:       15
        src-successors:  [ 14 ]
        dst-successors:  [ 14 ]
      - name:            14
        type:            progress
        src-block:       task1_for.cond17
        dst-block:       16
        src-successors:  [ 15, 16 ]
        dst-successors:  [ 15, 16 ]
      - name:            15
        type:            progress
        src-block:       task1_for.body19
        dst-block:       17
        src-successors:  [ 25 ]
        dst-successors:  [ 25 ]
      - name:            16
        type:            progress
        src-block:       task1_for.end22.cc_loopend
        dst-block:       19
        src-successors:  [ 17 ]
        dst-successors:  [ 17 ]
      - name:            17
        type:            progress
        src-block:       task1_for.end22
        dst-block:       20
        src-successors:  [ 18 ]
        dst-successors:  [ 18 ]
      - name:            18
        type:            progress
        src-block:       task1_for.cond24.cc_loopbegin
        dst-block:       21
        src-successors:  [ 19 ]
        dst-successors:  [ 19 ]
      - name:            19
        type:            progress
        src-block:       task1_for.cond24
        dst-block:       22
        src-successors:  [ 20, 21 ]
        dst-successors:  [ 20, 21 ]
      - name:            20
        type:            progress
        src-block:       task1_for.body26
        dst-block:       23
        src-successors:  [ 24 ]
        dst-successors:  [ 24 ]
      - name:            21
        type:            progress
        src-block:       task1_for.end29.cc_loopend
        dst-block:       25
        src-successors:  [ 22 ]
        dst-successors:  [ 22 ]
      - name:            22
        type:            progress
        src-block:       task1_for.end29
        dst-block:       26
        src-successors:  [ 23 ]
        dst-successors:  [ 23 ]
      - name:            23
        type:            progress
        src-block:       task1_for.end29.PSplit.0
        dst-block:       27
        src-successors:  [ 1 ]
        dst-successors:  [ 1 ]
      - name:            24
        type:            progress
        src-block:       task1_for.inc27
        dst-block:       24
        src-successors:  [ 19 ]
        dst-successors:  [ 19 ]
      - name:            25
        type:            progress
        src-block:       task1_for.inc20
        dst-block:       18
        src-successors:  [ 14 ]
        dst-successors:  [ 14 ]
      - name:            26
        type:            progress
        src-block:       task1_for.inc12
        dst-block:       13
        src-successors:  [ 10 ]
        dst-successors:  [ 10 ]
      - name:            27
        type:            progress
        src-block:       task1_for.inc5
        dst-block:       8
        src-successors:  [ 6 ]
        dst-successors:  [ 6 ]
      - name:            28
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
        src-hint:        'task1:8'
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
        src-hint:        'task1:11'
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
        src-hint:        'task1:12'
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
        src-hint:        'task1:11'
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
        src-hint:        'task1:16'
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
        src-hint:        'task1:16'
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
        src-hint:        'task1:17'
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
        src-hint:        'task1:16'
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
        src-hint:        'task1:21'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            10
        mapsto:          task1_for.end7
        predecessors:    [ 9 ]
        successors:      [ 11 ]
        src-hint:        'task1:21'
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
        src-hint:        'task1:21'
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
        src-hint:        'task1:22'
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
        src-hint:        'task1:21'
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
        src-hint:        'task1:25'
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
      - name:            15
        mapsto:          task1_for.cond17.cc_loopbegin
        predecessors:    [ 14 ]
        successors:      [ 16 ]
        src-hint:        'task1:28'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            16
        mapsto:          task1_for.cond17
        predecessors:    [ 15, 18 ]
        successors:      [ 17, 19 ]
        loops:           [ 16 ]
        src-hint:        'task1:28'
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
        mapsto:          task1_for.body19
        predecessors:    [ 16 ]
        successors:      [ 18 ]
        loops:           [ 16 ]
        src-hint:        'task1:29'
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
        mapsto:          task1_for.inc20
        predecessors:    [ 17 ]
        successors:      [ 16 ]
        loops:           [ 16 ]
        src-hint:        'task1:28'
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
        mapsto:          task1_for.end22.cc_loopend
        predecessors:    [ 16 ]
        successors:      [ 20 ]
        src-hint:        'task1:33'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            20
        mapsto:          task1_for.end22
        predecessors:    [ 19 ]
        successors:      [ 21 ]
        src-hint:        'task1:33'
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
        mapsto:          task1_for.cond24.cc_loopbegin
        predecessors:    [ 20 ]
        successors:      [ 22 ]
        src-hint:        'task1:33'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            22
        mapsto:          task1_for.cond24
        predecessors:    [ 21, 24 ]
        successors:      [ 23, 25 ]
        loops:           [ 22 ]
        src-hint:        'task1:33'
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
      - name:            23
        mapsto:          task1_for.body26
        predecessors:    [ 22 ]
        successors:      [ 24 ]
        loops:           [ 22 ]
        src-hint:        'task1:34'
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
      - name:            24
        mapsto:          task1_for.inc27
        predecessors:    [ 23 ]
        successors:      [ 22 ]
        loops:           [ 22 ]
        src-hint:        'task1:33'
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
      - name:            25
        mapsto:          task1_for.end29.cc_loopend
        predecessors:    [ 22 ]
        successors:      [ 26 ]
        src-hint:        'task1:37'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            26
        mapsto:          task1_for.end29
        predecessors:    [ 25 ]
        successors:      [ 27 ]
        src-hint:        'task1:37'
        instructions:
          - index:           0
            opcode:          PseudoCALL
            size:            8
            branch-type:     call
          - index:           1
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            27
        mapsto:          task1_for.end29.PSplit.0
        predecessors:    [ 26 ]
        successors:      [  ]
        src-hint:        'task1:38'
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
      - { entry-block: task1_for.body19, exit-block: task1_for.body19, 
          function: task1, index: 2 }
      - { entry-block: task1_for.body26, exit-block: task1_for.body26, 
          function: task1, index: 3 }
      - { entry-block: task1_for.body4, exit-block: task1_for.body4, function: task1, 
          index: 4 }
      - { entry-block: task1_for.cond17, exit-block: task1_for.cond17, 
          function: task1, index: 5 }
      - { entry-block: task1_for.cond17.cc_loopbegin, exit-block: task1_for.cond17.cc_loopbegin, 
          function: task1, index: 6 }
      - { entry-block: task1_for.cond2, exit-block: task1_for.cond2, function: task1, 
          index: 7 }
      - { entry-block: task1_for.cond2.cc_loopbegin, exit-block: task1_for.cond2.cc_loopbegin, 
          function: task1, index: 8 }
      - { entry-block: task1_for.cond24, exit-block: task1_for.cond24, 
          function: task1, index: 9 }
      - { entry-block: task1_for.cond24.cc_loopbegin, exit-block: task1_for.cond24.cc_loopbegin, 
          function: task1, index: 10 }
      - { entry-block: task1_for.end22, exit-block: task1_for.end22, function: task1, 
          index: 11 }
      - { entry-block: task1_for.end22.cc_loopend, exit-block: task1_for.end22.cc_loopend, 
          function: task1, index: 12 }
      - { entry-block: task1_for.end29, exit-block: task1_for.end29, function: task1, 
          index: 13 }
      - { entry-block: task1_for.end29.cc_loopend, exit-block: task1_for.end29.cc_loopend, 
          function: task1, index: 14 }
      - { entry-block: task1_for.end7, exit-block: task1_for.end14, function: task1, 
          index: 15 }
      - { entry-block: task1_for.end7.cc_loopend, exit-block: task1_for.end7.cc_loopend, 
          function: task1, index: 16 }
      - { entry-block: task1_for.inc20, exit-block: task1_for.inc20, function: task1, 
          index: 17 }
      - { entry-block: task1_for.inc27, exit-block: task1_for.inc27, function: task1, 
          index: 18 }
      - { entry-block: task1_for.inc5, exit-block: task1_for.inc5, function: task1, 
          index: 19 }
      - { entry-block: '', exit-block: '', function: '', index: 20 }
    devices:
      - { power: 105648000, index: 0, name: CpuHighFreq }
      - { power: 28483000, index: 1, name: CpuLowFreq }
      - { power: 0, index: 2, name: UartOn }
      - { power: 0, index: 3, name: OsDefault }
    entry-nodes:     [ 0 ]
    exit-nodes:      [ 38, 37 ]
    name:            pstg-main
    nodes:
      - pabb:            0
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 0 ]
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
        successor-edges: [ 1, 2 ]
        predecessor-edges: [ 0 ]
        input-constraint: { inputs: [ 0 ], potential-inputs: [  ] }
        index:           1
      - pabb:            2
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 26 ]
        predecessor-edges: [ 23 ]
        costs:           { time_ns: 110000, power_nW: 24832209 }
        input-constraint: { inputs: [ 23 ], potential-inputs: [  ] }
        index:           2
      - pabb:            2
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 54 ]
        predecessor-edges: [ 19 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 19 ], potential-inputs: [  ] }
        index:           3
      - pabb:            3
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 41 ]
        predecessor-edges: [ 38 ]
        costs:           { time_ns: 110000, power_nW: 24832209 }
        input-constraint: { inputs: [ 38 ], potential-inputs: [  ] }
        index:           4
      - pabb:            3
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 47 ]
        predecessor-edges: [ 34 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 34 ], potential-inputs: [  ] }
        index:           5
      - pabb:            4
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 11 ]
        predecessor-edges: [ 8 ]
        costs:           { time_ns: 110000, power_nW: 24832209 }
        input-constraint: { inputs: [ 8 ], potential-inputs: [  ] }
        index:           6
      - pabb:            4
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 61 ]
        predecessor-edges: [ 4 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 4 ], potential-inputs: [  ] }
        index:           7
      - pabb:            5
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 23, 24, 25 ]
        predecessor-edges: [ 12, 22, 53, 59 ]
        input-constraint: { inputs: [ 12, 22, 53, 59 ], potential-inputs: [  ] }
        index:           8
      - pabb:            5
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 18, 19, 20 ]
        predecessor-edges: [ 16, 21, 57, 58 ]
        input-constraint: { inputs: [ 16, 21, 57, 58 ], potential-inputs: [  ] }
        index:           9
      - pabb:            6
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 58, 59 ]
        predecessor-edges: [ 13 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 13 ], potential-inputs: [  ] }
        index:           10
      - pabb:            6
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 21, 22 ]
        predecessor-edges: [ 17 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 17 ], potential-inputs: [  ] }
        index:           11
      - pabb:            7
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 8, 9, 10 ]
        predecessor-edges: [ 7, 60 ]
        input-constraint: { inputs: [ 7, 60 ], potential-inputs: [  ] }
        index:           12
      - pabb:            7
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 3, 4, 5 ]
        predecessor-edges: [ 1, 6, 64 ]
        input-constraint: { inputs: [ 1, 6, 64 ], potential-inputs: [  ] }
        index:           13
      - pabb:            8
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 6, 7 ]
        predecessor-edges: [ 2 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 2 ], potential-inputs: [  ] }
        index:           14
      - pabb:            9
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 38, 39, 40 ]
        predecessor-edges: [ 27, 37, 46, 52 ]
        input-constraint: { inputs: [ 27, 37, 46, 52 ], potential-inputs: [  ] }
        index:           15
      - pabb:            9
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 33, 34, 35 ]
        predecessor-edges: [ 31, 36, 50, 51 ]
        input-constraint: { inputs: [ 31, 36, 50, 51 ], potential-inputs: [  ] }
        index:           16
      - pabb:            10
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 51, 52 ]
        predecessor-edges: [ 28 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 28 ], potential-inputs: [  ] }
        index:           17
      - pabb:            10
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 36, 37 ]
        predecessor-edges: [ 32 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 32 ], potential-inputs: [  ] }
        index:           18
      - pabb:            11
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 27, 28 ]
        predecessor-edges: [ 24, 29, 55 ]
        input-constraint: { inputs: [ 24, 29, 55 ], potential-inputs: [  ] }
        index:           19
      - pabb:            11
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 31, 32 ]
        predecessor-edges: [ 18, 30, 56 ]
        input-constraint: { inputs: [ 18, 30, 56 ], potential-inputs: [  ] }
        index:           20
      - pabb:            12
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 29, 30 ]
        predecessor-edges: [ 25 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 25 ], potential-inputs: [  ] }
        index:           21
      - pabb:            12
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 55, 56 ]
        predecessor-edges: [ 20 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 20 ], potential-inputs: [  ] }
        index:           22
      - pabb:            13
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 42 ]
        predecessor-edges: [ 39, 43, 48 ]
        input-constraint: { inputs: [ 39, 43, 48 ], potential-inputs: [  ] }
        index:           23
      - pabb:            13
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 45 ]
        predecessor-edges: [ 33, 44, 49 ]
        input-constraint: { inputs: [ 33, 44, 49 ], potential-inputs: [  ] }
        index:           24
      - pabb:            14
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 43, 44 ]
        predecessor-edges: [ 40 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 40 ], potential-inputs: [  ] }
        index:           25
      - pabb:            14
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 48, 49 ]
        predecessor-edges: [ 35 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 35 ], potential-inputs: [  ] }
        index:           26
      - pabb:            15
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 12, 13 ]
        predecessor-edges: [ 9, 14, 62 ]
        input-constraint: { inputs: [ 9, 14, 62 ], potential-inputs: [  ] }
        index:           27
      - pabb:            15
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 16, 17 ]
        predecessor-edges: [ 3, 15, 63 ]
        input-constraint: { inputs: [ 3, 15, 63 ], potential-inputs: [  ] }
        index:           28
      - pabb:            16
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 14, 15 ]
        predecessor-edges: [ 10 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 10 ], potential-inputs: [  ] }
        index:           29
      - pabb:            16
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 62, 63 ]
        predecessor-edges: [ 5 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 5 ], potential-inputs: [  ] }
        index:           30
      - pabb:            17
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 53 ]
        predecessor-edges: [ 26 ]
        input-constraint: { inputs: [ 26 ], potential-inputs: [  ] }
        index:           31
      - pabb:            17
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 57 ]
        predecessor-edges: [ 54 ]
        input-constraint: { inputs: [ 54 ], potential-inputs: [  ] }
        index:           32
      - pabb:            18
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 46 ]
        predecessor-edges: [ 41 ]
        input-constraint: { inputs: [ 41 ], potential-inputs: [  ] }
        index:           33
      - pabb:            18
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 50 ]
        predecessor-edges: [ 47 ]
        input-constraint: { inputs: [ 47 ], potential-inputs: [  ] }
        index:           34
      - pabb:            19
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 60 ]
        predecessor-edges: [ 11 ]
        input-constraint: { inputs: [ 11 ], potential-inputs: [  ] }
        index:           35
      - pabb:            19
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 64 ]
        predecessor-edges: [ 61 ]
        input-constraint: { inputs: [ 61 ], potential-inputs: [  ] }
        index:           36
      - pabb:            20
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 42 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 42 ], potential-inputs: [  ] }
        index:           37
      - pabb:            20
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 45 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 45 ], potential-inputs: [  ] }
        index:           38
    edges:
      - index:           0
        source:          0
        target:          1
      - index:           1
        source:          1
        target:          13
      - index:           2
        source:          1
        target:          14
      - index:           3
        source:          13
        target:          28
      - index:           4
        source:          13
        target:          7
      - index:           5
        source:          13
        target:          30
      - index:           6
        source:          14
        target:          13
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           7
        source:          14
        target:          12
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           8
        source:          12
        target:          6
      - index:           9
        source:          12
        target:          27
      - index:           10
        source:          12
        target:          29
      - index:           11
        source:          6
        target:          35
      - index:           12
        source:          27
        target:          8
      - index:           13
        source:          27
        target:          10
      - index:           14
        source:          29
        target:          27
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           15
        source:          29
        target:          28
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           16
        source:          28
        target:          9
      - index:           17
        source:          28
        target:          11
      - index:           18
        source:          9
        target:          20
      - index:           19
        source:          9
        target:          3
      - index:           20
        source:          9
        target:          22
      - index:           21
        source:          11
        target:          9
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           22
        source:          11
        target:          8
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           23
        source:          8
        target:          2
      - index:           24
        source:          8
        target:          19
      - index:           25
        source:          8
        target:          21
      - index:           26
        source:          2
        target:          31
      - index:           27
        source:          19
        target:          15
      - index:           28
        source:          19
        target:          17
      - index:           29
        source:          21
        target:          19
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           30
        source:          21
        target:          20
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           31
        source:          20
        target:          16
      - index:           32
        source:          20
        target:          18
      - index:           33
        source:          16
        target:          24
      - index:           34
        source:          16
        target:          5
      - index:           35
        source:          16
        target:          26
      - index:           36
        source:          18
        target:          16
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           37
        source:          18
        target:          15
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           38
        source:          15
        target:          4
      - index:           39
        source:          15
        target:          23
      - index:           40
        source:          15
        target:          25
      - index:           41
        source:          4
        target:          33
      - index:           42
        source:          23
        target:          37
      - index:           43
        source:          25
        target:          23
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           44
        source:          25
        target:          24
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           45
        source:          24
        target:          38
      - index:           46
        source:          33
        target:          15
      - index:           47
        source:          5
        target:          34
      - index:           48
        source:          26
        target:          23
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           49
        source:          26
        target:          24
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           50
        source:          34
        target:          16
      - index:           51
        source:          17
        target:          16
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           52
        source:          17
        target:          15
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           53
        source:          31
        target:          8
      - index:           54
        source:          3
        target:          32
      - index:           55
        source:          22
        target:          19
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           56
        source:          22
        target:          20
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           57
        source:          32
        target:          9
      - index:           58
        source:          10
        target:          9
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           59
        source:          10
        target:          8
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           60
        source:          35
        target:          12
      - index:           61
        source:          7
        target:          36
      - index:           62
        source:          30
        target:          27
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           63
        source:          30
        target:          28
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           64
        source:          36
        target:          13
    transition-constraints:
      - { index: 0, left: [ 0 ], right: [ 1, 2 ] }
      - { index: 1, left: [ 23 ], right: [ 26 ] }
      - { index: 2, left: [ 19 ], right: [ 54 ] }
      - { index: 3, left: [ 38 ], right: [ 41 ] }
      - { index: 4, left: [ 34 ], right: [ 47 ] }
      - { index: 5, left: [ 8 ], right: [ 11 ] }
      - { index: 6, left: [ 4 ], right: [ 61 ] }
      - { index: 7, left: [ 12, 22, 53, 59 ], right: [ 23, 24, 25 ] }
      - { index: 8, left: [ 16, 21, 57, 58 ], right: [ 18, 19, 20 ] }
      - { index: 9, left: [ 13 ], right: [ 58, 59 ] }
      - { index: 10, left: [ 17 ], right: [ 21, 22 ] }
      - { index: 11, left: [ 7, 60 ], right: [ 8, 9, 10 ] }
      - { index: 12, left: [ 1, 6, 64 ], right: [ 3, 4, 5 ] }
      - { index: 13, left: [ 2 ], right: [ 6, 7 ] }
      - { index: 14, left: [ 27, 37, 46, 52 ], right: [ 38, 39, 40 ] }
      - { index: 15, left: [ 31, 36, 50, 51 ], right: [ 33, 34, 35 ] }
      - { index: 16, left: [ 28 ], right: [ 51, 52 ] }
      - { index: 17, left: [ 32 ], right: [ 36, 37 ] }
      - { index: 18, left: [ 24, 29, 55 ], right: [ 27, 28 ] }
      - { index: 19, left: [ 18, 30, 56 ], right: [ 31, 32 ] }
      - { index: 20, left: [ 25 ], right: [ 29, 30 ] }
      - { index: 21, left: [ 20 ], right: [ 55, 56 ] }
      - { index: 22, left: [ 39, 43, 48 ], right: [ 42 ] }
      - { index: 23, left: [ 33, 44, 49 ], right: [ 45 ] }
      - { index: 24, left: [ 40 ], right: [ 43, 44 ] }
      - { index: 25, left: [ 35 ], right: [ 48, 49 ] }
      - { index: 26, left: [ 9, 14, 62 ], right: [ 12, 13 ] }
      - { index: 27, left: [ 3, 15, 63 ], right: [ 16, 17 ] }
      - { index: 28, left: [ 10 ], right: [ 14, 15 ] }
      - { index: 29, left: [ 5 ], right: [ 62, 63 ] }
      - { index: 30, left: [ 26 ], right: [ 53 ] }
      - { index: 31, left: [ 54 ], right: [ 57 ] }
      - { index: 32, left: [ 41 ], right: [ 46 ] }
      - { index: 33, left: [ 47 ], right: [ 50 ] }
      - { index: 34, left: [ 11 ], right: [ 60 ] }
      - { index: 35, left: [ 61 ], right: [ 64 ] }
    loop-constraints:
      - { index: 0, backlink: [ 8, 9, 10, 11, 12, 13, 14, 23, 24, 25, 26, 
                                27, 28, 29, 38, 39, 40, 41, 42, 43, 46, 
                                52, 53, 59, 60 ], entry: [ 7, 22, 37, 48, 
                                                           55, 62 ] }
      - { index: 1, backlink: [ 50 ], entry: [ 31, 36, 51 ] }
      - { index: 2, backlink: [ 46 ], entry: [ 27, 37, 52 ] }
      - { index: 3, backlink: [ 57 ], entry: [ 16, 21, 58 ] }
      - { index: 4, backlink: [ 53 ], entry: [ 12, 22, 59 ] }
      - { index: 5, backlink: [ 64 ], entry: [ 1, 6 ] }
      - { index: 6, backlink: [ 60 ], entry: [ 7 ] }
    upper-bound-constraints:
      - { index: 0, upper-bound: 900, backlink-edges: [ 50, 46 ], entry-edges: [ 
                                                                                 31, 
                                                                                 36, 
                                                                                 51, 
                                                                                 27, 
                                                                                 37, 
                                                                                 52 ] }
      - { index: 1, upper-bound: 900, backlink-edges: [ 57, 53 ], entry-edges: [ 
                                                                                 16, 
                                                                                 21, 
                                                                                 58, 
                                                                                 12, 
                                                                                 22, 
                                                                                 59 ] }
      - { index: 2, upper-bound: 900, backlink-edges: [ 64, 60 ], entry-edges: [ 
                                                                                 1, 
                                                                                 6, 
                                                                                 7 ] }
    cc-alternatives:
      - cc-nodes:        [ 11, 10 ]
        alternatives:
          - { edges: [ 12, 16 ] }
          - { edges: [ 21, 58 ] }
          - { edges: [ 22, 59 ] }
      - cc-nodes:        [ 14 ]
        alternatives:
          - { edges: [ 1 ] }
          - { edges: [ 6 ] }
          - { edges: [ 7 ] }
      - cc-nodes:        [ 18, 17 ]
        alternatives:
          - { edges: [ 27, 31 ] }
          - { edges: [ 36, 51 ] }
          - { edges: [ 37, 52 ] }
      - cc-nodes:        [ 21, 22 ]
        alternatives:
          - { edges: [ 18, 24 ] }
          - { edges: [ 30, 56 ] }
          - { edges: [ 29, 55 ] }
      - cc-nodes:        [ 25, 26 ]
        alternatives:
          - { edges: [ 33, 39 ] }
          - { edges: [ 44, 49 ] }
          - { edges: [ 43, 48 ] }
      - cc-nodes:        [ 29, 30 ]
        alternatives:
          - { edges: [ 3, 9 ] }
          - { edges: [ 15, 63 ] }
          - { edges: [ 14, 62 ] }
...
