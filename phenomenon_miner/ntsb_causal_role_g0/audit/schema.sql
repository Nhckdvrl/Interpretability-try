-- ----------------------------------------------------------
-- MDB Tools - A library for reading MS Access database files
-- Copyright (C) 2000-2011 Brian Bruns and others.
-- Files in libmdb are licensed under LGPL and the utilities under
-- the GPL, see COPYING.LIB and COPYING files respectively.
-- Check out http://mdbtools.sourceforge.net
-- ----------------------------------------------------------

-- That file uses encoding ISO-8859-1

CREATE TABLE [Country]
 (
	[COUNTRY_CODE]			Text (3), 
	[COUNTRY_NAME]			Text (50)
);

CREATE TABLE [ct_iaids]
 (
	[ct_name]			Text (22), 
	[code_iaids]			Text (4), 
	[meaning]			Text (50), 
	[seq]			Integer, 
	[ntsb_type]			Text (1), 
	[ntsb_code]			Text (2), 
	[avn_code]			Text (5), 
	[ntsb_codes_more]			Text (11), 
	[not_for_ntsb_use]			Boolean NOT NULL, 
	[eADMS_use]			Boolean NOT NULL, 
	[notes]			Text (50)
);

CREATE TABLE [ct_seqevt]
 (
	[code]			Long Integer, 
	[meaning]			Text (50)
);

CREATE TABLE [dt_events]
 (
	[ev_id]			Text (14) NOT NULL, 
	[col_name]			Text (20) NOT NULL, 
	[code]			Text (4) NOT NULL, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);

CREATE TABLE [dt_Flight_Crew]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[crew_no]			Byte NOT NULL, 
	[col_name]			Text (20) NOT NULL, 
	[code]			Text (4) NOT NULL, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);

CREATE TABLE [eADMSPUB_DataDictionary]
 (
	[Category of Data]			Text (255), 
	[Table]			Text (255), 
	[Column]			Text (255), 
	[ct_name]			Text (255), 
	[code_iaids]			Text (255), 
	[meaning]			Text (255), 
	[Data Type eADMS]			Text (255), 
	[Length eADMS]			Double, 
	[short_desc]			Text (255), 
	[Question_Def]			Memo/Hyperlink (255), 
	[Code meaning]			Memo/Hyperlink (255), 
	[typeofchange]			Text (25), 
	[Change_notes]			Memo/Hyperlink (255)
);

CREATE TABLE [engines]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[eng_no]			Integer NOT NULL, 
	[eng_type]			Text (4), 
	[eng_mfgr]			Text (30), 
	[eng_model]			Text (13), 
	[power_units]			Long Integer, 
	[hp_or_lbs]			Text (4), 
	[lchg_userid]			Text (18), 
	[lchg_date]			DateTime, 
	[carb_fuel_injection]			Text (4), 
	[propeller_type]			Text (4), 
	[propeller_make]			Text (50), 
	[propeller_model]			Text (50), 
	[eng_time_total]			Single, 
	[eng_time_last_insp]			Single, 
	[eng_time_overhaul]			Single
);

CREATE TABLE [events]
 (
	[ev_id]			Text (14) NOT NULL, 
	[ntsb_no]			Text (10), 
	[ev_type]			Text (3), 
	[ev_date]			DateTime, 
	[ev_dow]			Text (2), 
	[ev_time]			Integer, 
	[ev_tmzn]			Text (3), 
	[ev_city]			Text (50), 
	[ev_state]			Text (2), 
	[ev_country]			Text (4), 
	[ev_site_zipcode]			Text (10), 
	[ev_year]			Integer, 
	[ev_month]			Byte, 
	[mid_air]			Text (1), 
	[on_ground_collision]			Text (1), 
	[latitude]			Text (7), 
	[longitude]			Text (8), 
	[latlong_acq]			Text (4), 
	[apt_name]			Text (30), 
	[ev_nr_apt_id]			Text (4), 
	[ev_nr_apt_loc]			Text (4), 
	[apt_dist]			Single, 
	[apt_dir]			Integer, 
	[apt_elev]			Integer, 
	[wx_brief_comp]			Text (4), 
	[wx_src_iic]			Text (4), 
	[wx_obs_time]			Integer, 
	[wx_obs_dir]			Integer, 
	[wx_obs_fac_id]			Text (4), 
	[wx_obs_elev]			Long Integer, 
	[wx_obs_dist]			Integer, 
	[wx_obs_tmzn]			Text (3), 
	[light_cond]			Text (4), 
	[sky_cond_nonceil]			Text (4), 
	[sky_nonceil_ht]			Long Integer, 
	[sky_ceil_ht]			Long Integer, 
	[sky_cond_ceil]			Text (4), 
	[vis_rvr]			Single, 
	[vis_rvv]			Integer, 
	[vis_sm]			Single, 
	[wx_temp]			Integer, 
	[wx_dew_pt]			Integer, 
	[wind_dir_deg]			Integer, 
	[wind_dir_ind]			Text (1), 
	[wind_vel_kts]			Byte, 
	[wind_vel_ind]			Text (4), 
	[gust_ind]			Text (1), 
	[gust_kts]			Integer, 
	[altimeter]			Single, 
	[wx_dens_alt]			Long Integer, 
	[wx_int_precip]			Text (3), 
	[metar]			Memo/Hyperlink (255), 
	[ev_highest_injury]			Text (4), 
	[inj_f_grnd]			Integer, 
	[inj_m_grnd]			Integer, 
	[inj_s_grnd]			Integer, 
	[inj_tot_f]			Integer, 
	[inj_tot_m]			Integer, 
	[inj_tot_n]			Integer, 
	[inj_tot_s]			Integer, 
	[inj_tot_t]			Integer, 
	[invest_agy]			Text (1), 
	[ntsb_docket]			Long Integer, 
	[ntsb_notf_from]			Text (30), 
	[ntsb_notf_date]			DateTime, 
	[ntsb_notf_tm]			Integer, 
	[fiche_number]			Text (5), 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18), 
	[wx_cond_basic]			Text (3), 
	[faa_dist_office]			Text (50), 
	[dec_latitude]			Double, 
	[dec_longitude]			Double
);

CREATE TABLE [Events_Sequence]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[Occurrence_No]			Long Integer NOT NULL, 
	[Occurrence_Code]			Text (7), 
	[Occurrence_Description]			Text (100), 
	[phase_no]			Text (3), 
	[eventsoe_no]			Text (3), 
	[Defining_ev]			Boolean NOT NULL, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);

CREATE TABLE [Flight_Crew]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[crew_no]			Byte NOT NULL, 
	[crew_category]			Text (5), 
	[crew_age]			Byte, 
	[crew_sex]			Text (1), 
	[crew_city]			Text (15), 
	[crew_res_state]			Text (2), 
	[crew_res_country]			Text (4), 
	[med_certf]			Text (4), 
	[med_crtf_vldty]			Text (4), 
	[date_lst_med]			DateTime, 
	[crew_rat_endorse]			Text (1), 
	[crew_inj_level]			Text (4), 
	[seatbelts_used]			Text (1), 
	[shldr_harn_used]			Text (1), 
	[crew_tox_perf]			Text (1), 
	[seat_occ_pic]			Text (4), 
	[pc_profession]			Text (4), 
	[bfr]			Text (1), 
	[bfr_date]			DateTime, 
	[ft_as_of]			DateTime, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18), 
	[seat_occ_row]			Long Integer, 
	[infl_rest_inst]			Text (1), 
	[infl_rest_depl]			Text (1), 
	[child_restraint]			Text (3), 
	[med_crtf_limit]			Memo/Hyperlink (255), 
	[mr_faa_med_certf]			Text (4), 
	[pilot_flying]			Boolean NOT NULL, 
	[available_restraint]			Text (1), 
	[restraint_used]			Text (1)
);

CREATE TABLE [flight_time]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[crew_no]			Byte NOT NULL, 
	[flight_type]			Text (4) NOT NULL, 
	[flight_craft]			Text (4) NOT NULL, 
	[flight_hours]			Single, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);

CREATE TABLE [injury]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[inj_person_category]			Text (4) NOT NULL, 
	[injury_level]			Text (4) NOT NULL, 
	[inj_person_count]			Integer, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);

CREATE TABLE [NTSB_Admin]
 (
	[ev_id]			Text (14), 
	[rec_stat]			Text (1), 
	[approval_date]			DateTime, 
	[lchg_userid]			Text (18), 
	[lchg_date]			DateTime
);

CREATE TABLE [Occurrences]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[Occurrence_No]			Long Integer NOT NULL, 
	[Occurrence_Code]			Long Integer, 
	[Phase_of_Flight]			Long Integer, 
	[Altitude]			Long Integer, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);

CREATE TABLE [seq_of_events]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[Occurrence_No]			Long Integer NOT NULL, 
	[seq_event_no]			Long Integer NOT NULL, 
	[group_code]			Integer NOT NULL, 
	[Subj_Code]			Long Integer, 
	[Cause_Factor]			Text (1), 
	[Modifier_Code]			Long Integer, 
	[Person_Code]			Long Integer, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);

CREATE TABLE [states]
 (
	[state]			Text (2) NOT NULL, 
	[name]			Text (30) NOT NULL, 
	[faa_region]			Text (2) NOT NULL
);

CREATE TABLE [aircraft]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[regis_no]			Text (11), 
	[ntsb_no]			Text (11), 
	[acft_missing]			Text (1), 
	[far_part]			Text (4), 
	[flt_plan_filed]			Text (4), 
	[flight_plan_activated]			Text (1), 
	[damage]			Text (4), 
	[acft_fire]			Text (4), 
	[acft_expl]			Text (4), 
	[acft_make]			Text (30), 
	[acft_model]			Text (20), 
	[acft_series]			Text (10), 
	[acft_serial_no]			Text (20), 
	[cert_max_gr_wt]			Long Integer, 
	[acft_category]			Text (4), 
	[acft_reg_cls]			Text (4), 
	[homebuilt]			Text (3), 
	[fc_seats]			Long Integer, 
	[cc_seats]			Long Integer, 
	[pax_seats]			Long Integer, 
	[total_seats]			Integer, 
	[num_eng]			Byte, 
	[fixed_retractable]			Text (4), 
	[type_last_insp]			Text (4), 
	[date_last_insp]			DateTime, 
	[afm_hrs_last_insp]			Single, 
	[afm_hrs]			Single, 
	[elt_install]			Text (1), 
	[elt_oper]			Text (1), 
	[elt_aided_loc_ev]			Text (1), 
	[elt_type]			Text (4), 
	[owner_acft]			Text (50), 
	[owner_street]			Text (50), 
	[owner_city]			Text (50), 
	[owner_state]			Text (2), 
	[owner_country]			Text (4), 
	[owner_zip]			Text (10), 
	[oper_individual_name]			Text (1), 
	[oper_name]			Text (50), 
	[oper_same]			Text (1), 
	[oper_dba]			Text (50), 
	[oper_addr_same]			Text (1), 
	[oper_street]			Text (50), 
	[oper_city]			Text (50), 
	[oper_state]			Text (2), 
	[oper_country]			Text (4), 
	[oper_zip]			Text (10), 
	[oper_code]			Text (4), 
	[certs_held]			Text (1), 
	[oprtng_cert]			Text (3), 
	[oper_cert]			Text (4), 
	[oper_cert_num]			Text (11), 
	[oper_sched]			Text (4), 
	[oper_dom_int]			Text (3), 
	[oper_pax_cargo]			Text (4), 
	[type_fly]			Text (4), 
	[second_pilot]			Text (1), 
	[dprt_pt_same_ev]			Text (1), 
	[dprt_apt_id]			Text (4), 
	[dprt_city]			Text (50), 
	[dprt_state]			Text (2), 
	[dprt_country]			Text (3), 
	[dprt_time]			Integer, 
	[dprt_timezn]			Text (3), 
	[dest_same_local]			Text (4), 
	[dest_apt_id]			Text (4), 
	[dest_city]			Text (50), 
	[dest_state]			Text (2), 
	[dest_country]			Text (3), 
	[phase_flt_spec]			Long Integer, 
	[report_to_icao]			Text (1), 
	[evacuation]			Text (1), 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18), 
	[afm_hrs_since]			Text (4), 
	[rwy_num]			Text (4), 
	[rwy_len]			Long Integer, 
	[rwy_width]			Long Integer, 
	[site_seeing]			Text (1), 
	[air_medical]			Text (1), 
	[med_type_flight]			Text (15), 
	[acft_year]			Long Integer, 
	[fuel_on_board]			Text (20), 
	[commercial_space_flight]			Boolean NOT NULL, 
	[unmanned]			Boolean NOT NULL, 
	[ifr_equipped_cert]			Boolean NOT NULL, 
	[elt_mounted_aircraft]			Boolean NOT NULL, 
	[elt_connected_antenna]			Boolean NOT NULL, 
	[elt_manufacturer]			Text (50), 
	[elt_model]			Text (50), 
	[elt_reason_other]			Memo/Hyperlink (255)
);

CREATE TABLE [dt_aircraft]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[col_name]			Text (20) NOT NULL, 
	[code]			Text (4) NOT NULL, 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);

CREATE TABLE [Findings]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[finding_no]			Long Integer NOT NULL, 
	[finding_code]			Text (10), 
	[finding_description]			Text (255), 
	[category_no]			Text (2), 
	[subcategory_no]			Text (2), 
	[section_no]			Text (2), 
	[subsection_no]			Text (2), 
	[modifier_no]			Text (2), 
	[Cause_Factor]			Text (1), 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (50), 
	[cm_inPc]			Text (1)
);

CREATE TABLE [narratives]
 (
	[ev_id]			Text (14) NOT NULL, 
	[Aircraft_Key]			Long Integer NOT NULL, 
	[narr_accp]			Memo/Hyperlink (255), 
	[narr_accf]			Memo/Hyperlink (255), 
	[narr_cause]			Memo/Hyperlink (255), 
	[narr_inc]			Memo/Hyperlink (255), 
	[lchg_date]			DateTime, 
	[lchg_userid]			Text (18)
);


