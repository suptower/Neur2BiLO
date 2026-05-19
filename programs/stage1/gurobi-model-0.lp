\ Model ilp
\ LP format - for model browsing. Use MPS format to capture full model detail.
\ Signature: 0x688ec0d1b4ffd6d2
Maximize
  objective
Subject To
 pstg_entry_node: N0 = 1
 pstg_entry_edge: N0->N1(14) = 1
 pstg_exit_edges: N8->N14(15) + N7->N13(11) = 1
 pstg_inflow_N1: N0->N1(14) - N1 = 0
 pstg_inflow_N2: - N2 + N4->N2(7) = 0
 pstg_inflow_N3: - N3 + N5->N3(3) = 0
 pstg_inflow_N4: N11->N4(16) - N4 + N6->N4(6) = 0
 pstg_inflow_N5: N6->N5(5) + N12->N5(20) - N5 + N1->N5(0) = 0
 pstg_inflow_N6: - N6 + N1->N6(1) = 0
 pstg_inflow_N7: N10->N7(18) + N4->N7(8) + N9->N7(12) - N7 = 0
 pstg_inflow_N8: N5->N8(2) - N8 + N9->N8(13) + N10->N8(19) = 0
 pstg_inflow_N9: - N9 + N4->N9(9) = 0
 pstg_inflow_N10: N5->N10(4) - N10 = 0
 pstg_inflow_N11: N2->N11(10) - N11 = 0
 pstg_inflow_N12: - N12 + N3->N12(17) = 0
 pstg_inflow_N13: N7->N13(11) - N13 = 0
 pstg_inflow_N14: N8->N14(15) - N14 = 0
 pstg-time: 102000 N10->N7(18) + 89000 N3 - global-timing + 56 N12
   + 1501 N6->N5(5) + 68 N5 + 110000 N2 + 56 N8 + 2250 N11
   + 22000 N9->N8(13) + 1501 N10->N8(19) + 20000 N9->N7(12) + 484618 N1
   + 2750 N4 + 102000 N6->N4(6) + 2250 N7 = 0
 pstg_tc_0: - N0->N1(14) + N1->N6(1) + N1->N5(0) = 0
 pstg_tc_1: - N4->N2(7) + N2->N11(10) = 0
 pstg_tc_2: N3->N12(17) - N5->N3(3) = 0
 pstg_tc_3: N4->N7(8) + N4->N2(7) - N11->N4(16) + N4->N9(9) - N6->N4(6)
   = 0
 pstg_tc_4: N5->N8(2) - N6->N5(5) - N12->N5(20) + N5->N10(4) - N1->N5(0)
   + N5->N3(3) = 0
 pstg_tc_5: N6->N5(5) - N1->N6(1) + N6->N4(6) = 0
 pstg_tc_6: - N10->N7(18) - N4->N7(8) + N7->N13(11) - N9->N7(12) = 0
 pstg_tc_7: N8->N14(15) - N5->N8(2) - N9->N8(13) - N10->N8(19) = 0
 pstg_tc_8: N9->N8(13) + N9->N7(12) - N4->N9(9) = 0
 pstg_tc_9: N10->N7(18) - N5->N10(4) + N10->N8(19) = 0
 pstg_tc_10: - N2->N11(10) + N11->N4(16) = 0
 pstg_tc_11: - N3->N12(17) + N12->N5(20) = 0
 pstg_loop_constraint_0: - 1e+06 N10->N7(18) + N4->N7(8) + N7->N13(11)
   + N4->N2(7) + N2->N11(10) + N11->N4(16) + N9->N7(12) + N4->N9(9)
   - 1e+06 N6->N4(6) <= 0
 pstg_loop_constraint_1: - 1e+06 N6->N5(5) + N12->N5(20) - 1e+06 N1->N5(0)
   <= 0
 pstg_loop_constraint_2: N11->N4(16) - 1e+06 N6->N4(6) <= 0
 pstg_upper_bound_0: - 900 N6->N5(5) + N12->N5(20) + N11->N4(16)
   - 900 N1->N5(0) - 900 N6->N4(6) <= 0
 cc_alt_cstr_0: - cc_alt_vars_0 + N1->N5(0) = 0
 cc_alt_cstr_1: N6->N5(5) - cc_alt_vars_1 = 0
 cc_alt_cstr_2: - cc_alt_vars_2 + N6->N4(6) = 0
 cc_alt_cstr_3: N5->N8(2) + N4->N7(8) - cc_alt_vars_3 = 0
 cc_alt_cstr_4: - cc_alt_vars_4 + N9->N8(13) + N10->N8(19) = 0
 cc_alt_cstr_5: N10->N7(18) - cc_alt_vars_5 + N9->N7(12) = 0
 objective_constraint: - 5826.130962 N10->N7(18) - 8182.438034 N3
   - 5.916288 N12 - 307.800304494 N6->N5(5) - 7.184064 N5 - 2731.54299 N2
   - 5.916288 N8 - 64.08674999999999 N11 - 617.54 N9->N8(13)
   - 307.800304494 N10->N8(19) - 493.52632 N9->N7(12) - 51198.922464 N1
   - 78.32825 N4 - 5826.130962 N6->N4(6) - 64.08674999999999 N7 + objective
   = 0
Bounds
Generals
 N8->N14(15) N10->N7(18) cc_alt_vars_0 cc_alt_vars_5 cc_alt_vars_4
 N5->N8(2) N3 global-timing N0 N6 N12 N6->N5(5) N4->N7(8) N9 N0->N1(14)
 N7->N13(11) N3->N12(17) N12->N5(20) cc_alt_vars_1 N5 N1->N6(1) N2 N8
 N4->N2(7) N5->N10(4) N2->N11(10) N11 N9->N8(13) N14 N10->N8(19)
 cc_alt_vars_2 N11->N4(16) N9->N7(12) cc_alt_vars_3 N4->N9(9) N1->N5(0) N1
 N5->N3(3) N4 N10 N6->N4(6) N7 N13
Scenario 0
Bounds
 cc_alt_vars_5 <= 0
 cc_alt_vars_4 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_2 <= 0
Scenario 1
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_4 <= 0
 cc_alt_vars_2 <= 0
Scenario 2
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_4 <= 0
 cc_alt_vars_1 <= 0
Scenario 3
Bounds
 cc_alt_vars_5 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_2 <= 0
 cc_alt_vars_3 <= 0
Scenario 4
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_2 <= 0
 cc_alt_vars_3 <= 0
Scenario 5
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_5 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_3 <= 0
Scenario 6
Bounds
 cc_alt_vars_4 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_2 <= 0
 cc_alt_vars_3 <= 0
Scenario 7
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_4 <= 0
 cc_alt_vars_2 <= 0
 cc_alt_vars_3 <= 0
Scenario 8
Bounds
 cc_alt_vars_0 <= 0
 cc_alt_vars_4 <= 0
 cc_alt_vars_1 <= 0
 cc_alt_vars_3 <= 0
End
