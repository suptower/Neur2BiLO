\ Model ilp
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x688ec0d1b4ffd6d2
Maximize
  objective
Subject To
 pstg_entry_node: N0 = 1
 pstg_entry_edge: N0->N1(0) = 1
 pstg_exit_edges: N7->N13(10) + N8->N14(15) = 1
 pstg_inflow_N1: N0->N1(0) - N1 = 0
 pstg_inflow_N2: - N2 + N4->N2(6) = 0
 pstg_inflow_N3: N5->N3(2) - N3 = 0
 pstg_inflow_N4: N11->N4(16) - N4 + N6->N4(5) = 0
 pstg_inflow_N5: N6->N5(4) + N1->N5(13) - N5 + N12->N5(20) = 0
 pstg_inflow_N6: N1->N6(14) - N6 = 0
 pstg_inflow_N7: N4->N7(7) + N10->N7(18) - N7 + N9->N7(11) = 0
 pstg_inflow_N8: N5->N8(1) + N10->N8(19) - N8 + N9->N8(12) = 0
 pstg_inflow_N9: N4->N9(8) - N9 = 0
 pstg_inflow_N10: N5->N10(3) - N10 = 0
 pstg_inflow_N11: - N11 + N2->N11(9) = 0
 pstg_inflow_N12: - N12 + N3->N12(17) = 0
 pstg_inflow_N13: N7->N13(10) - N13 = 0
 pstg_inflow_N14: - N14 + N8->N14(15) = 0
 pstg-time: 56 N12 + 1501 N6->N5(4) + 1501 N10->N8(19) + 110000 N2
   - global-timing + 68 N5 + 2250 N11 + 56 N8 + 22000 N9->N8(12)
   + 102000 N10->N7(18) + 2750 N4 + 1.000356e+06 N1 + 2250 N7
   + 102000 N6->N4(5) + 20000 N9->N7(11) + 89000 N3 = 0
 pstg_tc_0: N1->N5(13) - N0->N1(0) + N1->N6(14) = 0
 pstg_tc_1: - N4->N2(6) + N2->N11(9) = 0
 pstg_tc_2: - N5->N3(2) + N3->N12(17) = 0
 pstg_tc_3: N4->N7(7) - N11->N4(16) + N4->N2(6) - N6->N4(5) + N4->N9(8)
   = 0
 pstg_tc_4: N5->N8(1) - N6->N5(4) - N1->N5(13) + N5->N10(3) + N5->N3(2)
   - N12->N5(20) = 0
 pstg_tc_5: N6->N5(4) + N6->N4(5) - N1->N6(14) = 0
 pstg_tc_6: N7->N13(10) - N4->N7(7) - N10->N7(18) - N9->N7(11) = 0
 pstg_tc_7: - N5->N8(1) - N10->N8(19) + N8->N14(15) - N9->N8(12) = 0
 pstg_tc_8: N9->N8(12) - N4->N9(8) + N9->N7(11) = 0
 pstg_tc_9: N10->N8(19) - N5->N10(3) + N10->N7(18) = 0
 pstg_tc_10: N11->N4(16) - N2->N11(9) = 0
 pstg_tc_11: - N3->N12(17) + N12->N5(20) = 0
 pstg_loop_constraint_0: N7->N13(10) + N4->N7(7) + N11->N4(16) + N4->N2(6)
   + N2->N11(9) - 1e+06 N10->N7(18) - 1e+06 N6->N4(5) + N4->N9(8)
   + N9->N7(11) <= 0
 pstg_loop_constraint_1: - 1e+06 N6->N5(4) - 1e+06 N1->N5(13) + N12->N5(20)
   <= 0
 pstg_loop_constraint_2: N11->N4(16) - 1e+06 N6->N4(5) <= 0
 pstg_upper_bound_0: - 900 N6->N5(4) - 900 N1->N5(13) + N11->N4(16)
   - 900 N6->N4(5) + N12->N5(20) <= 0
 cc_alt_cstr_0: - cc_alt_vars_0 + N1->N5(13) = 0
 cc_alt_cstr_1: N6->N5(4) - cc_alt_vars_1 = 0
 cc_alt_cstr_2: - cc_alt_vars_2 + N6->N4(5) = 0
 cc_alt_cstr_3: N5->N8(1) + N4->N7(7) - cc_alt_vars_3 = 0
 cc_alt_cstr_4: N10->N8(19) + N9->N8(12) - cc_alt_vars_4 = 0
 cc_alt_cstr_5: - cc_alt_vars_5 + N10->N7(18) + N9->N7(11) = 0
 objective_constraint: - 5.916288 N12 - 307.800304494 N6->N5(4)
   - 307.800304494 N10->N8(19) - 2731.54299 N2 - 7.184064 N5
   - 64.08674999999999 N11 - 5.916288 N8 - 617.54 N9->N8(12)
   - 5826.130962 N10->N7(18) - 78.32825 N4 - 105685.610688 N1
   - 64.08674999999999 N7 - 5826.130962 N6->N4(5) - 493.52632 N9->N7(11)
   - 8182.438034 N3 + objective = 0
Bounds
Generals
 N12 cc_alt_vars_0 N5->N8(1) N6->N5(4) N7->N13(10) N4->N7(7) N1->N5(13)
 N11->N4(16) cc_alt_vars_3 N10->N8(19) N2 global-timing N5 N11 N8 N14
 cc_alt_vars_5 N5->N10(3) N0->N1(0) N4->N2(6) cc_alt_vars_1 N2->N11(9)
 N8->N14(15) N9->N8(12) N10->N7(18) N4 cc_alt_vars_2 N1 N7 N10 N13
 N6->N4(5) N5->N3(2) N4->N9(8) N9->N7(11) N3->N12(17) N1->N6(14)
 N12->N5(20) cc_alt_vars_4 N0 N3 N9 N6
Scenario 0
Bounds
 cc_alt_vars_5 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_2 <= 0
 cc_alt_vars_4 <= 0
Scenario 1
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_2 <= 0
 cc_alt_vars_4 <= 0
Scenario 2
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_4 <= 0
Scenario 3
Bounds
 cc_alt_vars_3 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_2 <= 0
Scenario 4
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_3 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_2 <= 0
Scenario 5
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_3 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_1 <= 0
Scenario 6
Bounds
 cc_alt_vars_3 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_2 <= 0
 cc_alt_vars_4 <= 0
Scenario 7
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_3 <= 0
 cc_alt_vars_2 <= 0
 cc_alt_vars_4 <= 0
Scenario 8
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_3 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_4 <= 0
End
