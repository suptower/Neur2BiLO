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
            opcode:          alloca
          - index:           7
            opcode:          call
          - index:           8
            opcode:          store
            memmode:         store
          - index:           9
            opcode:          call
          - index:           10
            opcode:          store
            memmode:         store
          - index:           11
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
          - task1_for.cond31.cc_loopbegin
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond31.cc_loopbegin
        predecessors:
          - task1_for.end29
        successors:
          - task1_for.cond31
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.cond31
        predecessors:
          - task1_for.inc34
          - task1_for.cond31.cc_loopbegin
        successors:
          - task1_for.body33
          - task1_for.end36.cc_loopend
        loops:
          - task1_for.cond31
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
      - name:            task1_for.body33
        predecessors:
          - task1_for.cond31
        successors:
          - task1_for.inc34
        loops:
          - task1_for.cond31
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.inc34
        predecessors:
          - task1_for.body33
        successors:
          - task1_for.cond31
        loops:
          - task1_for.cond31
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
      - name:            task1_for.end36.cc_loopend
        predecessors:
          - task1_for.cond31
        successors:
          - task1_for.end36
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.end36
        predecessors:
          - task1_for.end36.cc_loopend
        successors:
          - task1_for.end36.PSplit.0
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.end36.PSplit.0
        predecessors:
          - task1_for.end36
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
  - scope:
      function:        task1
      loop:            task1_for.cond31
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond31
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
        src-successors:  [ 34 ]
        dst-successors:  [ 34 ]
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
        src-successors:  [ 33 ]
        dst-successors:  [ 33 ]
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
        src-successors:  [ 32 ]
        dst-successors:  [ 32 ]
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
        src-successors:  [ 31 ]
        dst-successors:  [ 31 ]
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
        src-successors:  [ 30 ]
        dst-successors:  [ 30 ]
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
        src-block:       task1_for.cond31.cc_loopbegin
        dst-block:       27
        src-successors:  [ 24 ]
        dst-successors:  [ 24 ]
      - name:            24
        type:            progress
        src-block:       task1_for.cond31
        dst-block:       28
        src-successors:  [ 25, 26 ]
        dst-successors:  [ 25, 26 ]
      - name:            25
        type:            progress
        src-block:       task1_for.body33
        dst-block:       29
        src-successors:  [ 29 ]
        dst-successors:  [ 29 ]
      - name:            26
        type:            progress
        src-block:       task1_for.end36.cc_loopend
        dst-block:       31
        src-successors:  [ 27 ]
        dst-successors:  [ 27 ]
      - name:            27
        type:            progress
        src-block:       task1_for.end36
        dst-block:       32
        src-successors:  [ 28 ]
        dst-successors:  [ 28 ]
      - name:            28
        type:            progress
        src-block:       task1_for.end36.PSplit.0
        dst-block:       33
        src-successors:  [ 1 ]
        dst-successors:  [ 1 ]
      - name:            29
        type:            progress
        src-block:       task1_for.inc34
        dst-block:       30
        src-successors:  [ 24 ]
        dst-successors:  [ 24 ]
      - name:            30
        type:            progress
        src-block:       task1_for.inc27
        dst-block:       24
        src-successors:  [ 19 ]
        dst-successors:  [ 19 ]
      - name:            31
        type:            progress
        src-block:       task1_for.inc20
        dst-block:       18
        src-successors:  [ 14 ]
        dst-successors:  [ 14 ]
      - name:            32
        type:            progress
        src-block:       task1_for.inc12
        dst-block:       13
        src-successors:  [ 10 ]
        dst-successors:  [ 10 ]
      - name:            33
        type:            progress
        src-block:       task1_for.inc5
        dst-block:       8
        src-successors:  [ 6 ]
        dst-successors:  [ 6 ]
      - name:            34
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
        src-hint:        'task1:38'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            26
        mapsto:          task1_for.end29
        predecessors:    [ 25 ]
        successors:      [ 27 ]
        src-hint:        'task1:38'
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
      - name:            27
        mapsto:          task1_for.cond31.cc_loopbegin
        predecessors:    [ 26 ]
        successors:      [ 28 ]
        src-hint:        'task1:38'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            28
        mapsto:          task1_for.cond31
        predecessors:    [ 27, 30 ]
        successors:      [ 29, 31 ]
        loops:           [ 28 ]
        src-hint:        'task1:38'
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
      - name:            29
        mapsto:          task1_for.body33
        predecessors:    [ 28 ]
        successors:      [ 30 ]
        loops:           [ 28 ]
        src-hint:        'task1:39'
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
      - name:            30
        mapsto:          task1_for.inc34
        predecessors:    [ 29 ]
        successors:      [ 28 ]
        loops:           [ 28 ]
        src-hint:        'task1:38'
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
      - name:            31
        mapsto:          task1_for.end36.cc_loopend
        predecessors:    [ 28 ]
        successors:      [ 32 ]
        src-hint:        'task1:42'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            32
        mapsto:          task1_for.end36
        predecessors:    [ 31 ]
        successors:      [ 33 ]
        src-hint:        'task1:42'
        instructions:
          - index:           0
            opcode:          PseudoCALL
            size:            8
            branch-type:     call
          - index:           1
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            33
        mapsto:          task1_for.end36.PSplit.0
        predecessors:    [ 32 ]
        successors:      [  ]
        src-hint:        'task1:43'
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
      - { entry-block: task1_for.body33, exit-block: task1_for.body33, 
          function: task1, index: 4 }
      - { entry-block: task1_for.body4, exit-block: task1_for.body4, function: task1, 
          index: 5 }
      - { entry-block: task1_for.cond17, exit-block: task1_for.cond17, 
          function: task1, index: 6 }
      - { entry-block: task1_for.cond17.cc_loopbegin, exit-block: task1_for.cond17.cc_loopbegin, 
          function: task1, index: 7 }
      - { entry-block: task1_for.cond2, exit-block: task1_for.cond2, function: task1, 
          index: 8 }
      - { entry-block: task1_for.cond2.cc_loopbegin, exit-block: task1_for.cond2.cc_loopbegin, 
          function: task1, index: 9 }
      - { entry-block: task1_for.cond24, exit-block: task1_for.cond24, 
          function: task1, index: 10 }
      - { entry-block: task1_for.cond24.cc_loopbegin, exit-block: task1_for.cond24.cc_loopbegin, 
          function: task1, index: 11 }
      - { entry-block: task1_for.cond31, exit-block: task1_for.cond31, 
          function: task1, index: 12 }
      - { entry-block: task1_for.cond31.cc_loopbegin, exit-block: task1_for.cond31.cc_loopbegin, 
          function: task1, index: 13 }
      - { entry-block: task1_for.end22, exit-block: task1_for.end22, function: task1, 
          index: 14 }
      - { entry-block: task1_for.end22.cc_loopend, exit-block: task1_for.end22.cc_loopend, 
          function: task1, index: 15 }
      - { entry-block: task1_for.end29, exit-block: task1_for.end29, function: task1, 
          index: 16 }
      - { entry-block: task1_for.end29.cc_loopend, exit-block: task1_for.end29.cc_loopend, 
          function: task1, index: 17 }
      - { entry-block: task1_for.end36, exit-block: task1_for.end36, function: task1, 
          index: 18 }
      - { entry-block: task1_for.end36.cc_loopend, exit-block: task1_for.end36.cc_loopend, 
          function: task1, index: 19 }
      - { entry-block: task1_for.end7, exit-block: task1_for.end14, function: task1, 
          index: 20 }
      - { entry-block: task1_for.end7.cc_loopend, exit-block: task1_for.end7.cc_loopend, 
          function: task1, index: 21 }
      - { entry-block: task1_for.inc20, exit-block: task1_for.inc20, function: task1, 
          index: 22 }
      - { entry-block: task1_for.inc27, exit-block: task1_for.inc27, function: task1, 
          index: 23 }
      - { entry-block: task1_for.inc34, exit-block: task1_for.inc34, function: task1, 
          index: 24 }
      - { entry-block: task1_for.inc5, exit-block: task1_for.inc5, function: task1, 
          index: 25 }
      - { entry-block: '', exit-block: '', function: '', index: 26 }
    devices:
      - { power: 105648000, index: 0, name: CpuHighFreq }
      - { power: 28483000, index: 1, name: CpuLowFreq }
      - { power: 0, index: 2, name: UartOn }
      - { power: 0, index: 3, name: OsDefault }
    entry-nodes:     [ 0 ]
    exit-nodes:      [ 50, 49 ]
    name:            pstg-main
    nodes:
      - pabb:            0
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 2 ]
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
        predecessor-edges: [ 2 ]
        input-constraint: { inputs: [ 2 ], potential-inputs: [  ] }
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
        successor-edges: [ 76 ]
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
        successor-edges: [ 69 ]
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
        successor-edges: [ 56 ]
        predecessor-edges: [ 53 ]
        costs:           { time_ns: 110000, power_nW: 24832209 }
        input-constraint: { inputs: [ 53 ], potential-inputs: [  ] }
        index:           6
      - pabb:            4
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 62 ]
        predecessor-edges: [ 49 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 49 ], potential-inputs: [  ] }
        index:           7
      - pabb:            5
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
        index:           8
      - pabb:            5
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 83 ]
        predecessor-edges: [ 4 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 4 ], potential-inputs: [  ] }
        index:           9
      - pabb:            6
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 23, 24, 25 ]
        predecessor-edges: [ 12, 22, 75, 81 ]
        input-constraint: { inputs: [ 12, 22, 75, 81 ], potential-inputs: [  ] }
        index:           10
      - pabb:            6
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 18, 19, 20 ]
        predecessor-edges: [ 16, 21, 79, 80 ]
        input-constraint: { inputs: [ 16, 21, 79, 80 ], potential-inputs: [  ] }
        index:           11
      - pabb:            7
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 80, 81 ]
        predecessor-edges: [ 13 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 13 ], potential-inputs: [  ] }
        index:           12
      - pabb:            7
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
        index:           13
      - pabb:            8
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 8, 9, 10 ]
        predecessor-edges: [ 7, 82 ]
        input-constraint: { inputs: [ 7, 82 ], potential-inputs: [  ] }
        index:           14
      - pabb:            8
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 3, 4, 5 ]
        predecessor-edges: [ 0, 6, 86 ]
        input-constraint: { inputs: [ 0, 6, 86 ], potential-inputs: [  ] }
        index:           15
      - pabb:            9
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 6, 7 ]
        predecessor-edges: [ 1 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 1 ], potential-inputs: [  ] }
        index:           16
      - pabb:            10
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 38, 39, 40 ]
        predecessor-edges: [ 27, 37, 68, 74 ]
        input-constraint: { inputs: [ 27, 37, 68, 74 ], potential-inputs: [  ] }
        index:           17
      - pabb:            10
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 33, 34, 35 ]
        predecessor-edges: [ 31, 36, 72, 73 ]
        input-constraint: { inputs: [ 31, 36, 72, 73 ], potential-inputs: [  ] }
        index:           18
      - pabb:            11
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 73, 74 ]
        predecessor-edges: [ 28 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 28 ], potential-inputs: [  ] }
        index:           19
      - pabb:            11
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
        index:           20
      - pabb:            12
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 53, 54, 55 ]
        predecessor-edges: [ 42, 52, 61, 67 ]
        input-constraint: { inputs: [ 42, 52, 61, 67 ], potential-inputs: [  ] }
        index:           21
      - pabb:            12
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 48, 49, 50 ]
        predecessor-edges: [ 46, 51, 65, 66 ]
        input-constraint: { inputs: [ 46, 51, 65, 66 ], potential-inputs: [  ] }
        index:           22
      - pabb:            13
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 66, 67 ]
        predecessor-edges: [ 43 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 43 ], potential-inputs: [  ] }
        index:           23
      - pabb:            13
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 51, 52 ]
        predecessor-edges: [ 47 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 47 ], potential-inputs: [  ] }
        index:           24
      - pabb:            14
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 27, 28 ]
        predecessor-edges: [ 24, 29, 77 ]
        input-constraint: { inputs: [ 24, 29, 77 ], potential-inputs: [  ] }
        index:           25
      - pabb:            14
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 31, 32 ]
        predecessor-edges: [ 18, 30, 78 ]
        input-constraint: { inputs: [ 18, 30, 78 ], potential-inputs: [  ] }
        index:           26
      - pabb:            15
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
        index:           27
      - pabb:            15
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 77, 78 ]
        predecessor-edges: [ 20 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 20 ], potential-inputs: [  ] }
        index:           28
      - pabb:            16
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 42, 43 ]
        predecessor-edges: [ 39, 44, 70 ]
        input-constraint: { inputs: [ 39, 44, 70 ], potential-inputs: [  ] }
        index:           29
      - pabb:            16
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 46, 47 ]
        predecessor-edges: [ 33, 45, 71 ]
        input-constraint: { inputs: [ 33, 45, 71 ], potential-inputs: [  ] }
        index:           30
      - pabb:            17
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 44, 45 ]
        predecessor-edges: [ 40 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 40 ], potential-inputs: [  ] }
        index:           31
      - pabb:            17
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 70, 71 ]
        predecessor-edges: [ 35 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 35 ], potential-inputs: [  ] }
        index:           32
      - pabb:            18
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 57 ]
        predecessor-edges: [ 54, 58, 63 ]
        input-constraint: { inputs: [ 54, 58, 63 ], potential-inputs: [  ] }
        index:           33
      - pabb:            18
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 60 ]
        predecessor-edges: [ 48, 59, 64 ]
        input-constraint: { inputs: [ 48, 59, 64 ], potential-inputs: [  ] }
        index:           34
      - pabb:            19
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 58, 59 ]
        predecessor-edges: [ 55 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 55 ], potential-inputs: [  ] }
        index:           35
      - pabb:            19
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 63, 64 ]
        predecessor-edges: [ 50 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 50 ], potential-inputs: [  ] }
        index:           36
      - pabb:            20
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 12, 13 ]
        predecessor-edges: [ 9, 14, 84 ]
        input-constraint: { inputs: [ 9, 14, 84 ], potential-inputs: [  ] }
        index:           37
      - pabb:            20
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 16, 17 ]
        predecessor-edges: [ 3, 15, 85 ]
        input-constraint: { inputs: [ 3, 15, 85 ], potential-inputs: [  ] }
        index:           38
      - pabb:            21
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
        index:           39
      - pabb:            21
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 84, 85 ]
        predecessor-edges: [ 5 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 5 ], potential-inputs: [  ] }
        index:           40
      - pabb:            22
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 75 ]
        predecessor-edges: [ 26 ]
        input-constraint: { inputs: [ 26 ], potential-inputs: [  ] }
        index:           41
      - pabb:            22
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 79 ]
        predecessor-edges: [ 76 ]
        input-constraint: { inputs: [ 76 ], potential-inputs: [  ] }
        index:           42
      - pabb:            23
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 68 ]
        predecessor-edges: [ 41 ]
        input-constraint: { inputs: [ 41 ], potential-inputs: [  ] }
        index:           43
      - pabb:            23
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 72 ]
        predecessor-edges: [ 69 ]
        input-constraint: { inputs: [ 69 ], potential-inputs: [  ] }
        index:           44
      - pabb:            24
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 61 ]
        predecessor-edges: [ 56 ]
        input-constraint: { inputs: [ 56 ], potential-inputs: [  ] }
        index:           45
      - pabb:            24
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 65 ]
        predecessor-edges: [ 62 ]
        input-constraint: { inputs: [ 62 ], potential-inputs: [  ] }
        index:           46
      - pabb:            25
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 82 ]
        predecessor-edges: [ 11 ]
        input-constraint: { inputs: [ 11 ], potential-inputs: [  ] }
        index:           47
      - pabb:            25
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 86 ]
        predecessor-edges: [ 83 ]
        input-constraint: { inputs: [ 83 ], potential-inputs: [  ] }
        index:           48
      - pabb:            26
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 57 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 57 ], potential-inputs: [  ] }
        index:           49
      - pabb:            26
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 60 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 60 ], potential-inputs: [  ] }
        index:           50
    edges:
      - index:           0
        source:          1
        target:          15
      - index:           1
        source:          1
        target:          16
      - index:           2
        source:          0
        target:          1
      - index:           3
        source:          15
        target:          38
      - index:           4
        source:          15
        target:          9
      - index:           5
        source:          15
        target:          40
      - index:           6
        source:          16
        target:          15
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           7
        source:          16
        target:          14
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           8
        source:          14
        target:          8
      - index:           9
        source:          14
        target:          37
      - index:           10
        source:          14
        target:          39
      - index:           11
        source:          8
        target:          47
      - index:           12
        source:          37
        target:          10
      - index:           13
        source:          37
        target:          12
      - index:           14
        source:          39
        target:          37
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           15
        source:          39
        target:          38
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           16
        source:          38
        target:          11
      - index:           17
        source:          38
        target:          13
      - index:           18
        source:          11
        target:          26
      - index:           19
        source:          11
        target:          3
      - index:           20
        source:          11
        target:          28
      - index:           21
        source:          13
        target:          11
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           22
        source:          13
        target:          10
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           23
        source:          10
        target:          2
      - index:           24
        source:          10
        target:          25
      - index:           25
        source:          10
        target:          27
      - index:           26
        source:          2
        target:          41
      - index:           27
        source:          25
        target:          17
      - index:           28
        source:          25
        target:          19
      - index:           29
        source:          27
        target:          25
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           30
        source:          27
        target:          26
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           31
        source:          26
        target:          18
      - index:           32
        source:          26
        target:          20
      - index:           33
        source:          18
        target:          30
      - index:           34
        source:          18
        target:          5
      - index:           35
        source:          18
        target:          32
      - index:           36
        source:          20
        target:          18
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           37
        source:          20
        target:          17
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           38
        source:          17
        target:          4
      - index:           39
        source:          17
        target:          29
      - index:           40
        source:          17
        target:          31
      - index:           41
        source:          4
        target:          43
      - index:           42
        source:          29
        target:          21
      - index:           43
        source:          29
        target:          23
      - index:           44
        source:          31
        target:          29
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           45
        source:          31
        target:          30
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           46
        source:          30
        target:          22
      - index:           47
        source:          30
        target:          24
      - index:           48
        source:          22
        target:          34
      - index:           49
        source:          22
        target:          7
      - index:           50
        source:          22
        target:          36
      - index:           51
        source:          24
        target:          22
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           52
        source:          24
        target:          21
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           53
        source:          21
        target:          6
      - index:           54
        source:          21
        target:          33
      - index:           55
        source:          21
        target:          35
      - index:           56
        source:          6
        target:          45
      - index:           57
        source:          33
        target:          49
      - index:           58
        source:          35
        target:          33
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           59
        source:          35
        target:          34
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           60
        source:          34
        target:          50
      - index:           61
        source:          45
        target:          21
      - index:           62
        source:          7
        target:          46
      - index:           63
        source:          36
        target:          33
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           64
        source:          36
        target:          34
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           65
        source:          46
        target:          22
      - index:           66
        source:          23
        target:          22
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           67
        source:          23
        target:          21
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           68
        source:          43
        target:          17
      - index:           69
        source:          5
        target:          44
      - index:           70
        source:          32
        target:          29
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           71
        source:          32
        target:          30
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           72
        source:          44
        target:          18
      - index:           73
        source:          19
        target:          18
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           74
        source:          19
        target:          17
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           75
        source:          41
        target:          10
      - index:           76
        source:          3
        target:          42
      - index:           77
        source:          28
        target:          25
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           78
        source:          28
        target:          26
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           79
        source:          42
        target:          11
      - index:           80
        source:          12
        target:          11
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           81
        source:          12
        target:          10
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           82
        source:          47
        target:          14
      - index:           83
        source:          9
        target:          48
      - index:           84
        source:          40
        target:          37
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           85
        source:          40
        target:          38
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           86
        source:          48
        target:          15
    transition-constraints:
      - { index: 0, left: [ 2 ], right: [ 0, 1 ] }
      - { index: 1, left: [ 23 ], right: [ 26 ] }
      - { index: 2, left: [ 19 ], right: [ 76 ] }
      - { index: 3, left: [ 38 ], right: [ 41 ] }
      - { index: 4, left: [ 34 ], right: [ 69 ] }
      - { index: 5, left: [ 53 ], right: [ 56 ] }
      - { index: 6, left: [ 49 ], right: [ 62 ] }
      - { index: 7, left: [ 8 ], right: [ 11 ] }
      - { index: 8, left: [ 4 ], right: [ 83 ] }
      - { index: 9, left: [ 12, 22, 75, 81 ], right: [ 23, 24, 25 ] }
      - { index: 10, left: [ 16, 21, 79, 80 ], right: [ 18, 19, 20 ] }
      - { index: 11, left: [ 13 ], right: [ 80, 81 ] }
      - { index: 12, left: [ 17 ], right: [ 21, 22 ] }
      - { index: 13, left: [ 7, 82 ], right: [ 8, 9, 10 ] }
      - { index: 14, left: [ 0, 6, 86 ], right: [ 3, 4, 5 ] }
      - { index: 15, left: [ 1 ], right: [ 6, 7 ] }
      - { index: 16, left: [ 27, 37, 68, 74 ], right: [ 38, 39, 40 ] }
      - { index: 17, left: [ 31, 36, 72, 73 ], right: [ 33, 34, 35 ] }
      - { index: 18, left: [ 28 ], right: [ 73, 74 ] }
      - { index: 19, left: [ 32 ], right: [ 36, 37 ] }
      - { index: 20, left: [ 42, 52, 61, 67 ], right: [ 53, 54, 55 ] }
      - { index: 21, left: [ 46, 51, 65, 66 ], right: [ 48, 49, 50 ] }
      - { index: 22, left: [ 43 ], right: [ 66, 67 ] }
      - { index: 23, left: [ 47 ], right: [ 51, 52 ] }
      - { index: 24, left: [ 24, 29, 77 ], right: [ 27, 28 ] }
      - { index: 25, left: [ 18, 30, 78 ], right: [ 31, 32 ] }
      - { index: 26, left: [ 25 ], right: [ 29, 30 ] }
      - { index: 27, left: [ 20 ], right: [ 77, 78 ] }
      - { index: 28, left: [ 39, 44, 70 ], right: [ 42, 43 ] }
      - { index: 29, left: [ 33, 45, 71 ], right: [ 46, 47 ] }
      - { index: 30, left: [ 40 ], right: [ 44, 45 ] }
      - { index: 31, left: [ 35 ], right: [ 70, 71 ] }
      - { index: 32, left: [ 54, 58, 63 ], right: [ 57 ] }
      - { index: 33, left: [ 48, 59, 64 ], right: [ 60 ] }
      - { index: 34, left: [ 55 ], right: [ 58, 59 ] }
      - { index: 35, left: [ 50 ], right: [ 63, 64 ] }
      - { index: 36, left: [ 9, 14, 84 ], right: [ 12, 13 ] }
      - { index: 37, left: [ 3, 15, 85 ], right: [ 16, 17 ] }
      - { index: 38, left: [ 10 ], right: [ 14, 15 ] }
      - { index: 39, left: [ 5 ], right: [ 84, 85 ] }
      - { index: 40, left: [ 26 ], right: [ 75 ] }
      - { index: 41, left: [ 76 ], right: [ 79 ] }
      - { index: 42, left: [ 41 ], right: [ 68 ] }
      - { index: 43, left: [ 69 ], right: [ 72 ] }
      - { index: 44, left: [ 56 ], right: [ 61 ] }
      - { index: 45, left: [ 62 ], right: [ 65 ] }
      - { index: 46, left: [ 11 ], right: [ 82 ] }
      - { index: 47, left: [ 83 ], right: [ 86 ] }
    loop-constraints:
      - { index: 0, backlink: [ 8, 9, 10, 11, 12, 13, 14, 23, 24, 25, 26, 
                                27, 28, 29, 38, 39, 40, 41, 42, 43, 44, 
                                53, 54, 55, 56, 57, 58, 61, 67, 68, 74, 
                                75, 81, 82 ], entry: [ 7, 22, 37, 52, 63, 
                                                       70, 77, 84 ] }
      - { index: 1, backlink: [ 65 ], entry: [ 46, 51, 66 ] }
      - { index: 2, backlink: [ 61 ], entry: [ 42, 52, 67 ] }
      - { index: 3, backlink: [ 72 ], entry: [ 31, 36, 73 ] }
      - { index: 4, backlink: [ 68 ], entry: [ 27, 37, 74 ] }
      - { index: 5, backlink: [ 79 ], entry: [ 16, 21, 80 ] }
      - { index: 6, backlink: [ 75 ], entry: [ 12, 22, 81 ] }
      - { index: 7, backlink: [ 86 ], entry: [ 0, 6 ] }
      - { index: 8, backlink: [ 82 ], entry: [ 7 ] }
    upper-bound-constraints:
      - { index: 0, upper-bound: 900, backlink-edges: [ 65, 61 ], entry-edges: [ 
                                                                                 46, 
                                                                                 51, 
                                                                                 66, 
                                                                                 42, 
                                                                                 52, 
                                                                                 67 ] }
      - { index: 1, upper-bound: 900, backlink-edges: [ 72, 68 ], entry-edges: [ 
                                                                                 31, 
                                                                                 36, 
                                                                                 73, 
                                                                                 27, 
                                                                                 37, 
                                                                                 74 ] }
      - { index: 2, upper-bound: 900, backlink-edges: [ 79, 75 ], entry-edges: [ 
                                                                                 16, 
                                                                                 21, 
                                                                                 80, 
                                                                                 12, 
                                                                                 22, 
                                                                                 81 ] }
      - { index: 3, upper-bound: 900, backlink-edges: [ 86, 82 ], entry-edges: [ 
                                                                                 0, 
                                                                                 6, 
                                                                                 7 ] }
    cc-alternatives:
      - cc-nodes:        [ 13, 12 ]
        alternatives:
          - { edges: [ 12, 16 ] }
          - { edges: [ 21, 80 ] }
          - { edges: [ 22, 81 ] }
      - cc-nodes:        [ 16 ]
        alternatives:
          - { edges: [ 0 ] }
          - { edges: [ 6 ] }
          - { edges: [ 7 ] }
      - cc-nodes:        [ 20, 19 ]
        alternatives:
          - { edges: [ 27, 31 ] }
          - { edges: [ 36, 73 ] }
          - { edges: [ 37, 74 ] }
      - cc-nodes:        [ 24, 23 ]
        alternatives:
          - { edges: [ 42, 46 ] }
          - { edges: [ 51, 66 ] }
          - { edges: [ 52, 67 ] }
      - cc-nodes:        [ 27, 28 ]
        alternatives:
          - { edges: [ 18, 24 ] }
          - { edges: [ 30, 78 ] }
          - { edges: [ 29, 77 ] }
      - cc-nodes:        [ 31, 32 ]
        alternatives:
          - { edges: [ 33, 39 ] }
          - { edges: [ 45, 71 ] }
          - { edges: [ 44, 70 ] }
      - cc-nodes:        [ 35, 36 ]
        alternatives:
          - { edges: [ 48, 54 ] }
          - { edges: [ 59, 64 ] }
          - { edges: [ 58, 63 ] }
      - cc-nodes:        [ 39, 40 ]
        alternatives:
          - { edges: [ 3, 9 ] }
          - { edges: [ 15, 85 ] }
          - { edges: [ 14, 84 ] }
...
