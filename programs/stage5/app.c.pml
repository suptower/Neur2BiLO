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
          - task1_for.cond.cc_loopbegin
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
      - name:            task1_for.cond.cc_loopbegin
        predecessors:
          - task1_entry
        successors:
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.cond
        predecessors:
          - task1_for.inc11
          - task1_for.cond.cc_loopbegin
        successors:
          - task1_for.body
          - task1_for.end13.cc_loopend
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
          - task1_for.cond1
        loops:
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond1
        predecessors:
          - task1_for.inc
          - task1_for.body
        successors:
          - task1_for.body3
          - task1_for.end
        loops:
          - task1_for.cond1
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
      - name:            task1_for.body3
        predecessors:
          - task1_for.cond1
        successors:
          - task1_for.inc
        loops:
          - task1_for.cond1
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
          - task1_for.body3
        successors:
          - task1_for.cond1
        loops:
          - task1_for.cond1
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
          - task1_for.cond1
        successors:
          - task1_for.cond5
        loops:
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond5
        predecessors:
          - task1_for.inc8
          - task1_for.end
        successors:
          - task1_for.body7
          - task1_for.end10
        loops:
          - task1_for.cond5
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
      - name:            task1_for.body7
        predecessors:
          - task1_for.cond5
        successors:
          - task1_for.inc8
        loops:
          - task1_for.cond5
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.inc8
        predecessors:
          - task1_for.body7
        successors:
          - task1_for.cond5
        loops:
          - task1_for.cond5
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
      - name:            task1_for.end10
        predecessors:
          - task1_for.cond5
        successors:
          - task1_for.inc11
        loops:
          - task1_for.cond
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.inc11
        predecessors:
          - task1_for.end10
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
      - name:            task1_for.end13.cc_loopend
        predecessors:
          - task1_for.cond
        successors:
          - task1_for.end13
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.end13
        predecessors:
          - task1_for.end13.cc_loopend
        successors:
          - task1_for.cond15
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond15
        predecessors:
          - task1_for.inc18
          - task1_for.end13
        successors:
          - task1_for.body17
          - task1_for.end20
        loops:
          - task1_for.cond15
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
      - name:            task1_for.body17
        predecessors:
          - task1_for.cond15
        successors:
          - task1_for.inc18
        loops:
          - task1_for.cond15
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
      - name:            task1_for.inc18
        predecessors:
          - task1_for.body17
        successors:
          - task1_for.cond15
        loops:
          - task1_for.cond15
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
      - name:            task1_for.end20
        predecessors:
          - task1_for.cond15
        successors:
          - task1_for.cond22.cc_loopbegin
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          store
            memmode:         store
          - index:           2
            opcode:          br
      - name:            task1_for.cond22.cc_loopbegin
        predecessors:
          - task1_for.end20
        successors:
          - task1_for.cond22
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.cond22
        predecessors:
          - task1_for.inc25
          - task1_for.cond22.cc_loopbegin
        successors:
          - task1_for.body24
          - task1_for.end27.cc_loopend
        loops:
          - task1_for.cond22
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
      - name:            task1_for.body24
        predecessors:
          - task1_for.cond22
        successors:
          - task1_for.inc25
        loops:
          - task1_for.cond22
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.inc25
        predecessors:
          - task1_for.body24
        successors:
          - task1_for.cond22
        loops:
          - task1_for.cond22
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
      - name:            task1_for.end27.cc_loopend
        predecessors:
          - task1_for.cond22
        successors:
          - task1_for.end27
        instructions:
          - index:           0
            opcode:          br
      - name:            task1_for.end27
        predecessors:
          - task1_for.end27.cc_loopend
        successors:
          - task1_for.end27.PSplit.1
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
      - name:            task1_for.end27.PSplit.1
        predecessors:
          - task1_for.end27
        successors:
          - task1_for.end27.PSplit.0
        instructions:
          - index:           0
            opcode:          call
          - index:           1
            opcode:          br
      - name:            task1_for.end27.PSplit.0
        predecessors:
          - task1_for.end27.PSplit.1
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
    rhs:             11
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
  - scope:
      function:        task1
      loop:            task1_for.cond1
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond1
    op:              less-equal
    rhs:             251
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
  - scope:
      function:        task1
      loop:            task1_for.cond5
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond5
    op:              less-equal
    rhs:             91
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
  - scope:
      function:        task1
      loop:            task1_for.cond15
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond15
    op:              less-equal
    rhs:             2501
    level:           bitcode
    origin:          user.bc
    classification:  loop-global
  - scope:
      function:        task1
      loop:            task1_for.cond22
    lhs:
      - factor:          1
        program-point:
          function:        task1
          block:           task1_for.cond22
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
        src-block:       task1_for.cond.cc_loopbegin
        dst-block:       1
        src-successors:  [ 3 ]
        dst-successors:  [ 3 ]
      - name:            3
        type:            progress
        src-block:       task1_for.cond
        dst-block:       2
        src-successors:  [ 4, 5 ]
        dst-successors:  [ 4, 5 ]
      - name:            4
        type:            progress
        src-block:       task1_for.body
        dst-block:       3
        src-successors:  [ 19 ]
        dst-successors:  [ 19 ]
      - name:            5
        type:            progress
        src-block:       task1_for.end13.cc_loopend
        dst-block:       13
        src-successors:  [ 6 ]
        dst-successors:  [ 6 ]
      - name:            6
        type:            progress
        src-block:       task1_for.end13
        dst-block:       14
        src-successors:  [ 7 ]
        dst-successors:  [ 7 ]
      - name:            7
        type:            progress
        src-block:       task1_for.cond15
        dst-block:       15
        src-successors:  [ 8, 9 ]
        dst-successors:  [ 8, 9 ]
      - name:            8
        type:            progress
        src-block:       task1_for.body17
        dst-block:       16
        src-successors:  [ 18 ]
        dst-successors:  [ 18 ]
      - name:            9
        type:            progress
        src-block:       task1_for.end20
        dst-block:       18
        src-successors:  [ 10 ]
        dst-successors:  [ 10 ]
      - name:            10
        type:            progress
        src-block:       task1_for.cond22.cc_loopbegin
        dst-block:       19
        src-successors:  [ 11 ]
        dst-successors:  [ 11 ]
      - name:            11
        type:            progress
        src-block:       task1_for.cond22
        dst-block:       20
        src-successors:  [ 12, 13 ]
        dst-successors:  [ 12, 13 ]
      - name:            12
        type:            progress
        src-block:       task1_for.body24
        dst-block:       21
        src-successors:  [ 17 ]
        dst-successors:  [ 17 ]
      - name:            13
        type:            progress
        src-block:       task1_for.end27.cc_loopend
        dst-block:       23
        src-successors:  [ 14 ]
        dst-successors:  [ 14 ]
      - name:            14
        type:            progress
        src-block:       task1_for.end27
        dst-block:       24
        src-successors:  [ 15 ]
        dst-successors:  [ 15 ]
      - name:            15
        type:            progress
        src-block:       task1_for.end27.PSplit.1
        dst-block:       25
        src-successors:  [ 16 ]
        dst-successors:  [ 16 ]
      - name:            16
        type:            progress
        src-block:       task1_for.end27.PSplit.0
        dst-block:       26
        src-successors:  [ 1 ]
        dst-successors:  [ 1 ]
      - name:            17
        type:            progress
        src-block:       task1_for.inc25
        dst-block:       22
        src-successors:  [ 11 ]
        dst-successors:  [ 11 ]
      - name:            18
        type:            progress
        src-block:       task1_for.inc18
        dst-block:       17
        src-successors:  [ 7 ]
        dst-successors:  [ 7 ]
      - name:            19
        type:            progress
        src-block:       task1_for.cond1
        dst-block:       4
        src-successors:  [ 20, 21 ]
        dst-successors:  [ 20, 21 ]
      - name:            20
        type:            progress
        src-block:       task1_for.body3
        dst-block:       5
        src-successors:  [ 27 ]
        dst-successors:  [ 27 ]
      - name:            21
        type:            progress
        src-block:       task1_for.end
        dst-block:       7
        src-successors:  [ 22 ]
        dst-successors:  [ 22 ]
      - name:            22
        type:            progress
        src-block:       task1_for.cond5
        dst-block:       8
        src-successors:  [ 23, 24 ]
        dst-successors:  [ 23, 24 ]
      - name:            23
        type:            progress
        src-block:       task1_for.body7
        dst-block:       9
        src-successors:  [ 26 ]
        dst-successors:  [ 26 ]
      - name:            24
        type:            progress
        src-block:       task1_for.end10
        dst-block:       11
        src-successors:  [ 25 ]
        dst-successors:  [ 25 ]
      - name:            25
        type:            progress
        src-block:       task1_for.inc11
        dst-block:       12
        src-successors:  [ 3 ]
        dst-successors:  [ 3 ]
      - name:            26
        type:            progress
        src-block:       task1_for.inc8
        dst-block:       10
        src-successors:  [ 22 ]
        dst-successors:  [ 22 ]
      - name:            27
        type:            progress
        src-block:       task1_for.inc
        dst-block:       6
        src-successors:  [ 19 ]
        dst-successors:  [ 19 ]
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
        mapsto:          task1_for.cond.cc_loopbegin
        predecessors:    [ 0 ]
        successors:      [ 2 ]
        src-hint:        'task1:12'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            2
        mapsto:          task1_for.cond
        predecessors:    [ 1, 12 ]
        successors:      [ 3, 13 ]
        loops:           [ 2 ]
        src-hint:        'task1:12'
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
      - name:            3
        mapsto:          task1_for.body
        predecessors:    [ 2 ]
        successors:      [ 4 ]
        loops:           [ 2 ]
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
      - name:            4
        mapsto:          task1_for.cond1
        predecessors:    [ 3, 6 ]
        successors:      [ 5, 7 ]
        loops:           [ 4, 2 ]
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
      - name:            5
        mapsto:          task1_for.body3
        predecessors:    [ 4 ]
        successors:      [ 6 ]
        loops:           [ 4, 2 ]
        src-hint:        'task1:17'
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
      - name:            6
        mapsto:          task1_for.inc
        predecessors:    [ 5 ]
        successors:      [ 4 ]
        loops:           [ 4, 2 ]
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
      - name:            7
        mapsto:          task1_for.end
        predecessors:    [ 4 ]
        successors:      [ 8 ]
        loops:           [ 2 ]
        src-hint:        'task1:22'
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
      - name:            8
        mapsto:          task1_for.cond5
        predecessors:    [ 7, 10 ]
        successors:      [ 9, 11 ]
        loops:           [ 8, 2 ]
        src-hint:        'task1:22'
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
      - name:            9
        mapsto:          task1_for.body7
        predecessors:    [ 8 ]
        successors:      [ 10 ]
        loops:           [ 8, 2 ]
        src-hint:        'task1:23'
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
      - name:            10
        mapsto:          task1_for.inc8
        predecessors:    [ 9 ]
        successors:      [ 8 ]
        loops:           [ 8, 2 ]
        src-hint:        'task1:22'
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
      - name:            11
        mapsto:          task1_for.end10
        predecessors:    [ 8 ]
        successors:      [ 12 ]
        loops:           [ 2 ]
        src-hint:        'task1:25'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            12
        mapsto:          task1_for.inc11
        predecessors:    [ 11 ]
        successors:      [ 2 ]
        loops:           [ 2 ]
        src-hint:        'task1:12'
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
      - name:            13
        mapsto:          task1_for.end13.cc_loopend
        predecessors:    [ 2 ]
        successors:      [ 14 ]
        src-hint:        'task1:29'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            14
        mapsto:          task1_for.end13
        predecessors:    [ 13 ]
        successors:      [ 15 ]
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
      - name:            15
        mapsto:          task1_for.cond15
        predecessors:    [ 14, 17 ]
        successors:      [ 16, 18 ]
        loops:           [ 15 ]
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
      - name:            16
        mapsto:          task1_for.body17
        predecessors:    [ 15 ]
        successors:      [ 17 ]
        loops:           [ 15 ]
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
      - name:            17
        mapsto:          task1_for.inc18
        predecessors:    [ 16 ]
        successors:      [ 15 ]
        loops:           [ 15 ]
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
      - name:            18
        mapsto:          task1_for.end20
        predecessors:    [ 15 ]
        successors:      [ 19 ]
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
      - name:            19
        mapsto:          task1_for.cond22.cc_loopbegin
        predecessors:    [ 18 ]
        successors:      [ 20 ]
        src-hint:        'task1:35'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            20
        mapsto:          task1_for.cond22
        predecessors:    [ 19, 22 ]
        successors:      [ 21, 23 ]
        loops:           [ 20 ]
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
      - name:            21
        mapsto:          task1_for.body24
        predecessors:    [ 20 ]
        successors:      [ 22 ]
        loops:           [ 20 ]
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
      - name:            22
        mapsto:          task1_for.inc25
        predecessors:    [ 21 ]
        successors:      [ 20 ]
        loops:           [ 20 ]
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
      - name:            23
        mapsto:          task1_for.end27.cc_loopend
        predecessors:    [ 20 ]
        successors:      [ 24 ]
        src-hint:        'task1:39'
        instructions:
          - index:           0
            opcode:          PseudoBR
            size:            4
            branch-type:     unconditional
      - name:            24
        mapsto:          task1_for.end27
        predecessors:    [ 23 ]
        successors:      [ 25 ]
        src-hint:        'task1:39'
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
        mapsto:          task1_for.end27.PSplit.1
        predecessors:    [ 24 ]
        successors:      [ 26 ]
        src-hint:        'task1:41'
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
        mapsto:          task1_for.end27.PSplit.0
        predecessors:    [ 25 ]
        successors:      [  ]
        src-hint:        'task1:42'
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
      - { entry-block: task1_entry, exit-block: task1_entry, function: task1, 
          index: 1 }
      - { entry-block: task1_for.body, exit-block: task1_for.body, function: task1, 
          index: 2 }
      - { entry-block: task1_for.body24, exit-block: task1_for.body24, 
          function: task1, index: 3 }
      - { entry-block: task1_for.body3, exit-block: task1_for.inc, function: task1, 
          index: 4 }
      - { entry-block: task1_for.body7, exit-block: task1_for.body7, function: task1, 
          index: 5 }
      - { entry-block: task1_for.cond, exit-block: task1_for.cond, function: task1, 
          index: 6 }
      - { entry-block: task1_for.cond.cc_loopbegin, exit-block: task1_for.cond.cc_loopbegin, 
          function: task1, index: 7 }
      - { entry-block: task1_for.cond1, exit-block: task1_for.cond1, function: task1, 
          index: 8 }
      - { entry-block: task1_for.cond22, exit-block: task1_for.cond22, 
          function: task1, index: 9 }
      - { entry-block: task1_for.cond22.cc_loopbegin, exit-block: task1_for.cond22.cc_loopbegin, 
          function: task1, index: 10 }
      - { entry-block: task1_for.cond5, exit-block: task1_for.cond5, function: task1, 
          index: 11 }
      - { entry-block: task1_for.end, exit-block: task1_for.end, function: task1, 
          index: 12 }
      - { entry-block: task1_for.end10, exit-block: task1_for.inc11, function: task1, 
          index: 13 }
      - { entry-block: task1_for.end13, exit-block: task1_for.end20, function: task1, 
          index: 14 }
      - { entry-block: task1_for.end13.cc_loopend, exit-block: task1_for.end13.cc_loopend, 
          function: task1, index: 15 }
      - { entry-block: task1_for.end27, exit-block: task1_for.end27, function: task1, 
          index: 16 }
      - { entry-block: task1_for.end27.PSplit.1, exit-block: task1_for.end27.PSplit.1, 
          function: task1, index: 17 }
      - { entry-block: task1_for.end27.cc_loopend, exit-block: task1_for.end27.cc_loopend, 
          function: task1, index: 18 }
      - { entry-block: task1_for.inc25, exit-block: task1_for.inc25, function: task1, 
          index: 19 }
      - { entry-block: task1_for.inc8, exit-block: task1_for.inc8, function: task1, 
          index: 20 }
      - { entry-block: '', exit-block: '', function: '', index: 21 }
    devices:
      - { power: 105648000, index: 0, name: CpuHighFreq }
      - { power: 28483000, index: 1, name: CpuLowFreq }
      - { power: 0, index: 2, name: UartOn }
      - { power: 0, index: 3, name: OsDefault }
    entry-nodes:     [ 0 ]
    exit-nodes:      [ 40, 39 ]
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
        successor-edges: [ 11 ]
        predecessor-edges: [ 8 ]
        input-constraint: { inputs: [ 8 ], potential-inputs: [  ] }
        index:           2
      - pabb:            2
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 49 ]
        predecessor-edges: [ 4 ]
        input-constraint: { inputs: [ 4 ], potential-inputs: [  ] }
        index:           3
      - pabb:            3
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
        index:           4
      - pabb:            3
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 34 ]
        predecessor-edges: [ 19 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 19 ], potential-inputs: [  ] }
        index:           5
      - pabb:            4
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 42 ]
        predecessor-edges: [ 40 ]
        input-constraint: { inputs: [ 40 ], potential-inputs: [  ] }
        index:           6
      - pabb:            4
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 54 ]
        predecessor-edges: [ 52 ]
        input-constraint: { inputs: [ 52 ], potential-inputs: [  ] }
        index:           7
      - pabb:            5
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 46 ]
        predecessor-edges: [ 44 ]
        costs:           { time_ns: 110000, power_nW: 24832209 }
        input-constraint: { inputs: [ 44 ], potential-inputs: [  ] }
        index:           8
      - pabb:            5
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 58 ]
        predecessor-edges: [ 56 ]
        costs:           { time_ns: 89000, power_nW: 91937506 }
        input-constraint: { inputs: [ 56 ], potential-inputs: [  ] }
        index:           9
      - pabb:            6
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 8, 9, 10 ]
        predecessor-edges: [ 7, 47 ]
        input-constraint: { inputs: [ 7, 47 ], potential-inputs: [  ] }
        index:           10
      - pabb:            6
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 3, 4, 5 ]
        predecessor-edges: [ 1, 6, 59 ]
        input-constraint: { inputs: [ 1, 6, 59 ], potential-inputs: [  ] }
        index:           11
      - pabb:            7
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
        index:           12
      - pabb:            8
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 40, 41 ]
        predecessor-edges: [ 11, 42 ]
        input-constraint: { inputs: [ 11, 42 ], potential-inputs: [  ] }
        index:           13
      - pabb:            8
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 52, 53 ]
        predecessor-edges: [ 49, 54 ]
        input-constraint: { inputs: [ 49, 54 ], potential-inputs: [  ] }
        index:           14
      - pabb:            9
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 23, 24, 25 ]
        predecessor-edges: [ 12, 22, 33, 39 ]
        input-constraint: { inputs: [ 12, 22, 33, 39 ], potential-inputs: [  ] }
        index:           15
      - pabb:            9
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 18, 19, 20 ]
        predecessor-edges: [ 16, 21, 37, 38 ]
        input-constraint: { inputs: [ 16, 21, 37, 38 ], potential-inputs: [  ] }
        index:           16
      - pabb:            10
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 38, 39 ]
        predecessor-edges: [ 13 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 13 ], potential-inputs: [  ] }
        index:           17
      - pabb:            10
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
        index:           18
      - pabb:            11
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 44, 45 ]
        predecessor-edges: [ 43, 48 ]
        input-constraint: { inputs: [ 43, 48 ], potential-inputs: [  ] }
        index:           19
      - pabb:            11
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 56, 57 ]
        predecessor-edges: [ 55, 60 ]
        input-constraint: { inputs: [ 55, 60 ], potential-inputs: [  ] }
        index:           20
      - pabb:            12
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 43 ]
        predecessor-edges: [ 41 ]
        input-constraint: { inputs: [ 41 ], potential-inputs: [  ] }
        index:           21
      - pabb:            12
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 55 ]
        predecessor-edges: [ 53 ]
        input-constraint: { inputs: [ 53 ], potential-inputs: [  ] }
        index:           22
      - pabb:            13
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 47 ]
        predecessor-edges: [ 45 ]
        input-constraint: { inputs: [ 45 ], potential-inputs: [  ] }
        index:           23
      - pabb:            13
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 59 ]
        predecessor-edges: [ 57 ]
        input-constraint: { inputs: [ 57 ], potential-inputs: [  ] }
        index:           24
      - pabb:            14
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 12, 13 ]
        predecessor-edges: [ 9, 14, 50 ]
        input-constraint: { inputs: [ 9, 14, 50 ], potential-inputs: [  ] }
        index:           25
      - pabb:            14
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 16, 17 ]
        predecessor-edges: [ 3, 15, 51 ]
        input-constraint: { inputs: [ 3, 15, 51 ], potential-inputs: [  ] }
        index:           26
      - pabb:            15
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
        index:           27
      - pabb:            15
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 50, 51 ]
        predecessor-edges: [ 5 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 5 ], potential-inputs: [  ] }
        index:           28
      - pabb:            16
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 27 ]
        predecessor-edges: [ 24, 28, 35 ]
        input-constraint: { inputs: [ 24, 28, 35 ], potential-inputs: [  ] }
        index:           29
      - pabb:            16
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 30 ]
        predecessor-edges: [ 18, 29, 36 ]
        input-constraint: { inputs: [ 18, 29, 36 ], potential-inputs: [  ] }
        index:           30
      - pabb:            17
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 32 ]
        predecessor-edges: [ 27 ]
        input-constraint: { inputs: [ 27 ], potential-inputs: [  ] }
        index:           31
      - pabb:            17
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 31 ]
        predecessor-edges: [ 30 ]
        input-constraint: { inputs: [ 30 ], potential-inputs: [  ] }
        index:           32
      - pabb:            18
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 28, 29 ]
        predecessor-edges: [ 25 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 25 ], potential-inputs: [  ] }
        index:           33
      - pabb:            18
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 35, 36 ]
        predecessor-edges: [ 20 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 20 ], potential-inputs: [  ] }
        index:           34
      - pabb:            19
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 33 ]
        predecessor-edges: [ 26 ]
        input-constraint: { inputs: [ 26 ], potential-inputs: [  ] }
        index:           35
      - pabb:            19
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 37 ]
        predecessor-edges: [ 34 ]
        input-constraint: { inputs: [ 34 ], potential-inputs: [  ] }
        index:           36
      - pabb:            20
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 48 ]
        predecessor-edges: [ 46 ]
        input-constraint: { inputs: [ 46 ], potential-inputs: [  ] }
        index:           37
      - pabb:            20
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [ 60 ]
        predecessor-edges: [ 58 ]
        input-constraint: { inputs: [ 58 ], potential-inputs: [  ] }
        index:           38
      - pabb:            21
        devices:         [ 1, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 4000000 }
          - { name: System_state, value: 1 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 32 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 32 ], potential-inputs: [  ] }
        index:           39
      - pabb:            21
        devices:         [ 0, 2, 3 ]
        variables:
          - { name: System_cpuFreq, value: 160000000 }
          - { name: System_state, value: 0 }
          - { name: UART_state, value: 0 }
          - { name: OS_state, value: 0 }
        successor-edges: [  ]
        predecessor-edges: [ 31 ]
        costs:           { time_ns: 0, power_nW: 0 }
        input-constraint: { inputs: [ 31 ], potential-inputs: [  ] }
        index:           40
    edges:
      - index:           0
        source:          0
        target:          1
      - index:           1
        source:          1
        target:          11
      - index:           2
        source:          1
        target:          12
      - index:           3
        source:          11
        target:          26
      - index:           4
        source:          11
        target:          3
      - index:           5
        source:          11
        target:          28
      - index:           6
        source:          12
        target:          11
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           7
        source:          12
        target:          10
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           8
        source:          10
        target:          2
      - index:           9
        source:          10
        target:          25
      - index:           10
        source:          10
        target:          27
      - index:           11
        source:          2
        target:          13
      - index:           12
        source:          25
        target:          15
      - index:           13
        source:          25
        target:          17
      - index:           14
        source:          27
        target:          25
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           15
        source:          27
        target:          26
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           16
        source:          26
        target:          16
      - index:           17
        source:          26
        target:          18
      - index:           18
        source:          16
        target:          30
      - index:           19
        source:          16
        target:          5
      - index:           20
        source:          16
        target:          34
      - index:           21
        source:          18
        target:          16
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           22
        source:          18
        target:          15
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           23
        source:          15
        target:          4
      - index:           24
        source:          15
        target:          29
      - index:           25
        source:          15
        target:          33
      - index:           26
        source:          4
        target:          35
      - index:           27
        source:          29
        target:          31
      - index:           28
        source:          33
        target:          29
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           29
        source:          33
        target:          30
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           30
        source:          30
        target:          32
      - index:           31
        source:          32
        target:          40
      - index:           32
        source:          31
        target:          39
      - index:           33
        source:          35
        target:          15
      - index:           34
        source:          5
        target:          36
      - index:           35
        source:          34
        target:          29
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           36
        source:          34
        target:          30
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           37
        source:          36
        target:          16
      - index:           38
        source:          17
        target:          16
        costs:           { time_ns: 22000, power_nW: 28070000 }
      - index:           39
        source:          17
        target:          15
        costs:           { time_ns: 20000, power_nW: 24676316 }
      - index:           40
        source:          13
        target:          6
      - index:           41
        source:          13
        target:          21
      - index:           42
        source:          6
        target:          13
      - index:           43
        source:          21
        target:          19
      - index:           44
        source:          19
        target:          8
      - index:           45
        source:          19
        target:          23
      - index:           46
        source:          8
        target:          37
      - index:           47
        source:          23
        target:          10
      - index:           48
        source:          37
        target:          19
      - index:           49
        source:          3
        target:          14
      - index:           50
        source:          28
        target:          25
        costs:           { time_ns: 102000, power_nW: 57118931 }
      - index:           51
        source:          28
        target:          26
        costs:           { time_ns: 1501, power_nW: 205063494 }
      - index:           52
        source:          14
        target:          7
      - index:           53
        source:          14
        target:          22
      - index:           54
        source:          7
        target:          14
      - index:           55
        source:          22
        target:          20
      - index:           56
        source:          20
        target:          9
      - index:           57
        source:          20
        target:          24
      - index:           58
        source:          9
        target:          38
      - index:           59
        source:          24
        target:          11
      - index:           60
        source:          38
        target:          20
    transition-constraints:
      - { index: 0, left: [ 0 ], right: [ 1, 2 ] }
      - { index: 1, left: [ 8 ], right: [ 11 ] }
      - { index: 2, left: [ 4 ], right: [ 49 ] }
      - { index: 3, left: [ 23 ], right: [ 26 ] }
      - { index: 4, left: [ 19 ], right: [ 34 ] }
      - { index: 5, left: [ 40 ], right: [ 42 ] }
      - { index: 6, left: [ 52 ], right: [ 54 ] }
      - { index: 7, left: [ 44 ], right: [ 46 ] }
      - { index: 8, left: [ 56 ], right: [ 58 ] }
      - { index: 9, left: [ 7, 47 ], right: [ 8, 9, 10 ] }
      - { index: 10, left: [ 1, 6, 59 ], right: [ 3, 4, 5 ] }
      - { index: 11, left: [ 2 ], right: [ 6, 7 ] }
      - { index: 12, left: [ 11, 42 ], right: [ 40, 41 ] }
      - { index: 13, left: [ 49, 54 ], right: [ 52, 53 ] }
      - { index: 14, left: [ 12, 22, 33, 39 ], right: [ 23, 24, 25 ] }
      - { index: 15, left: [ 16, 21, 37, 38 ], right: [ 18, 19, 20 ] }
      - { index: 16, left: [ 13 ], right: [ 38, 39 ] }
      - { index: 17, left: [ 17 ], right: [ 21, 22 ] }
      - { index: 18, left: [ 43, 48 ], right: [ 44, 45 ] }
      - { index: 19, left: [ 55, 60 ], right: [ 56, 57 ] }
      - { index: 20, left: [ 41 ], right: [ 43 ] }
      - { index: 21, left: [ 53 ], right: [ 55 ] }
      - { index: 22, left: [ 45 ], right: [ 47 ] }
      - { index: 23, left: [ 57 ], right: [ 59 ] }
      - { index: 24, left: [ 9, 14, 50 ], right: [ 12, 13 ] }
      - { index: 25, left: [ 3, 15, 51 ], right: [ 16, 17 ] }
      - { index: 26, left: [ 10 ], right: [ 14, 15 ] }
      - { index: 27, left: [ 5 ], right: [ 50, 51 ] }
      - { index: 28, left: [ 24, 28, 35 ], right: [ 27 ] }
      - { index: 29, left: [ 18, 29, 36 ], right: [ 30 ] }
      - { index: 30, left: [ 27 ], right: [ 32 ] }
      - { index: 31, left: [ 30 ], right: [ 31 ] }
      - { index: 32, left: [ 25 ], right: [ 28, 29 ] }
      - { index: 33, left: [ 20 ], right: [ 35, 36 ] }
      - { index: 34, left: [ 26 ], right: [ 33 ] }
      - { index: 35, left: [ 34 ], right: [ 37 ] }
      - { index: 36, left: [ 46 ], right: [ 48 ] }
      - { index: 37, left: [ 58 ], right: [ 60 ] }
    loop-constraints:
      - { index: 0, backlink: [ 8, 9, 10, 11, 12, 13, 14, 23, 24, 25, 26, 
                                27, 28, 32, 33, 39, 40, 41, 42, 43, 44, 
                                45, 46, 47, 48 ], entry: [ 7, 22, 35, 50 ] }
      - { index: 1, backlink: [ 48 ], entry: [ 43 ] }
      - { index: 2, backlink: [ 60 ], entry: [ 55 ] }
      - { index: 3, backlink: [ 42 ], entry: [ 11 ] }
      - { index: 4, backlink: [ 54 ], entry: [ 49 ] }
      - { index: 5, backlink: [ 37 ], entry: [ 16, 21, 38 ] }
      - { index: 6, backlink: [ 33 ], entry: [ 12, 22, 39 ] }
      - { index: 7, backlink: [ 59 ], entry: [ 1, 6 ] }
      - { index: 8, backlink: [ 47 ], entry: [ 7 ] }
    upper-bound-constraints:
      - { index: 0, upper-bound: 900, backlink-edges: [ 48, 60 ], entry-edges: [ 
                                                                                 43, 
                                                                                 55 ] }
      - { index: 1, upper-bound: 2500, backlink-edges: [ 42, 54 ], entry-edges: [ 
                                                                                  11, 
                                                                                  49 ] }
      - { index: 2, upper-bound: 900, backlink-edges: [ 37, 33 ], entry-edges: [ 
                                                                                 16, 
                                                                                 21, 
                                                                                 38, 
                                                                                 12, 
                                                                                 22, 
                                                                                 39 ] }
      - { index: 3, upper-bound: 10, backlink-edges: [ 59, 47 ], entry-edges: [ 
                                                                                1, 
                                                                                6, 
                                                                                7 ] }
    cc-alternatives:
      - cc-nodes:        [ 12 ]
        alternatives:
          - { edges: [ 1 ] }
          - { edges: [ 6 ] }
          - { edges: [ 7 ] }
      - cc-nodes:        [ 18, 17 ]
        alternatives:
          - { edges: [ 12, 16 ] }
          - { edges: [ 21, 38 ] }
          - { edges: [ 22, 39 ] }
      - cc-nodes:        [ 27, 28 ]
        alternatives:
          - { edges: [ 3, 9 ] }
          - { edges: [ 15, 51 ] }
          - { edges: [ 14, 50 ] }
      - cc-nodes:        [ 33, 34 ]
        alternatives:
          - { edges: [ 18, 24 ] }
          - { edges: [ 29, 36 ] }
          - { edges: [ 28, 35 ] }
...
