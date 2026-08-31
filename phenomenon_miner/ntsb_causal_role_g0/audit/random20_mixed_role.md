# Random-20 Mixed-Role Semantic / Leakage Audit

Seed: `20260831`  ·  drawn from 3506 mixed-role events (>=1 `C` and >=1 `F`).

Model-visible input is **only**: `narr_accp` (NTSB *Factual narrative*) + role-suffix-stripped `finding_description`. `Cause_Factor`, `cm_inPc`, `narr_cause` (probable cause) and `narr_accf` are audit-only.

---

## 1. `20090309X43538` — ERA09LA189

- date: `03/07/09 00:00:00`  year `2009`  type `ACC`
- location: Montauk, NY USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Directional control-Not attained/maintained | `C` | `0106202020` |
| 1 | 2 | `F` | `T` | Personnel issues-Action/decision-Action-Delayed action-Instructor/check pilot | `F` | `0204102540` |
| 1 | 3 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 368 words

> On March 7, 2009, about 1147 eastern standard time, a Cirrus SR-22, N574PG, crashed into a ditch during a simulated soft field takeoff at Montauk Airport (MTP), Montauk, New York. The certified flight instructor (CFI) and student pilot were not injured, and the airplane was substantially damaged. The flight was operated as a personal flight under the provisions of 14 Code of Federal Regulations Part 91, and no flight plan was filed. Visual meteorological conditions prevailed at the time of the accident. 
> 
> The student pilot stated that the CFI wanted him to do a simulated "short-field" takeoff. The student pilot pulled back on the elevator, added full power, and began the takeoff roll. As the airplane began to accelerate, the nose of the airplane rose, and he attempted to put the airplane into ground effect. The main gear touched down, and the airplane began to veer off of the runway. The student pilot stated that they both attempted to regain control of the airplane, but the right wing contacted the runway, and they collided with a ditch. The student pilot stated that he never let go of the controls after the instructor tried making a recovery. The student pilot did not report any mechanical problems or flight control anomalies with the airplane.
> 
> According to the CFI, he instructed his student to simulate a soft-field takeoff. He said that he instructed the student to begin the takeoff roll, rotate, and get the airplane into ground effect. The airplane climbed briefly, and then the main landing gear settled back down to the runway. The airplane began to roll and yaw to the right, and then collided with a ditch. The CFI stated that there was no positive exchange of flight controls with the student. The CFI did not report any mechanical problems or flight control anomalies with the airplane. In addition, he stated he had never demonstrated the accident maneuver to the student nor did he provide any formal ground instruction to the student on its execution.
> 
> Examination of the airplane by a Federal Aviation Administration inspector revealed flight control continuity throughout the airframe.
> 
> A weather observation at MTP about the time of the accident, indicated the wind was calm.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The student pilot's failure to maintain directional control during takeoff. Contributing to the accident was the instructor's delayed remedial action.

- duplicate stripped finding descriptions in this event: **0**

---

## 2. `20090201X30126` — WPR09CA105

- date: `02/01/09 00:00:00`  year `2009`  type `ACC`
- location: Bountiful, UT USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Climb rate-Capability exceeded | `C` | `0106203508` |
| 1 | 2 | `C` | `T` | Personnel issues-Action/decision-Info processing/decision-Decision making/judgment-Pilot | `C` | `0204152044` |
| 1 | 3 | `F` | `T` | Environmental issues-Physical environment-Terrain-Mountainous/hilly terrain-Effect on operation | `F` | `0302101082` |
| 1 | 4 | `F` | `T` | Environmental issues-Conditions/weather/phenomena-Wind-Tailwind-Effect on equipment | `F` | `0303401581` |
| 1 | 5 | `F` | `T` | Environmental issues-Conditions/weather/phenomena-Temp/humidity/pressure-High density altitude-Effect on equipment | `F` | `0303102081` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 138 words

> While en route to her destination, the pilot elected to fly the helicopter up a canyon toward rising terrain. Soon after making a "low pass" over a ridge above 8,000 feet mean sea level (MSL), the pilot increased collective in order to climb over upcoming terrain. As the collective was increased, the rotor RPM started to drop. The pilot immediately increased throttle, reversed course to fly downhill, and lowered the collective. During the turn, the helicopter encountered a quartering tailwind and began to settle toward the snow-covered terrain. Soon thereafter the helicopter contacted the terrain, but bounced back into the air. Immediately thereafter a main rotor blade severed the tail boom, and the helicopter impacted the terrain. According to the pilot, there was no evidence of an engine power loss or any anomaly with the flight control system.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's improper decision to fly at low altitude while maneuvering in mountainous terrain in a canyon and inadvertently exceeding the climb capability of the helicopter. Contributing to the accident were a high density altitude, mountainous terrain, and a tailwind encountered during the attempted course reversal.

- duplicate stripped finding descriptions in this event: **0**

---

## 3. `20130608X41116` — ERA13FA275

- date: `06/08/13 00:00:00`  year `2013`  type `ACC`
- location: Boynton Beach, FL USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `-` | `F` | Aircraft-Aircraft systems-Indicating/recording systems-Instrument panel-Failure | `-` | `0102311001` |
| 1 | 2 | `F` | `T` | Personnel issues-Action/decision-Info processing/decision-Decision making/judgment-Pilot | `F` | `0204152044` |
| 1 | 3 | `C` | `T` | Environmental issues-Conditions/weather/phenomena-Ceiling/visibility/precip-Below VFR minima-Effect on operation | `C` | `0303507582` |
| 1 | 4 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Airspeed-Not attained/maintained | `C` | `0106201020` |
| 1 | 5 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Angle of attack-Not attained/maintained | `C` | `0106204220` |
| 1 | 6 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 7 | `C` | `T` | Personnel issues-Psychological-Perception/orientation/illusion-Situational awareness-Pilot | `C` | `0202203544` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 3121 words

> HISTORY OF FLIGHTOn June 8, 2013, at 1002 eastern daylight time, a Cessna 340A, N217JP, was destroyed when it impacted shallow waters of the Loxahatchee National Wildlife Refuge, near Boynton Beach, Florida. The commercial pilot was fatally injured. Instrument meteorological conditions prevailed in the vicinity, and the airplane was operating on an instrument flight rules (IFR) flight plan from Fort Lauderdale Executive Airport (FXE), Fort Lauderdale, Florida, to Leesburg International Airport (LEE), Leesburg, Florida. The business flight was conducted under the provisions of 14 Code of Federal Regulations Part 91.
> 
> According to excerpts from the Federal Aviation Administration (FAA) Air Traffic Control Accident Package:
> 
> The pilot was cleared to depart FXE utilizing the Fort Lauderdale Three Departure to ARKES intersection, then direct to BAIRN intersection, then as filed [direct to LEE], climb to 2,000 feet, expect 16,000 feet 10 minutes after departure.
> 
> At 0945, the pilot was cleared to take off from FXE runway 8, and to then turn left to heading 310 degrees magnetic. After takeoff, the pilot was cleared to contact Miami Departure Control.
> 
> At 0947, the pilot advised Miami Departure Control that the airplane was passing 600 feet for 2,000 feet, in a left turn, heading 310 degrees. The departure controller advised radar contact, then cleared the airplane to 4,000 feet, which the pilot acknowledged.
> 
> At 0949, the pilot advised that he was having "instrument problems," and that he would like to "head west and stay v-f-r if I can for the climb." The controller confirmed with the pilot that the airplane was on an IFR flight plan, advised him of traffic ahead, told him to fly heading 270, and directed him switch to the next departure frequency, which the pilot acknowledged.
> 
> At 0950, the pilot contacted the next departure controller, who directed him to climb the airplane to 8,000 feet. The pilot responded that he would do so once he was clear of a cloud, and reiterated that he had "instrument problems." The controller acknowledged that the pilot would like to keep the airplane at 2,000 feet, and told the pilot to let him know when he could climb the airplane.
> 
> About 30 seconds later, the pilot stated that he was climbing the airplane to 8,000 feet, which the controller acknowledged.
> 
> Just before 0954, the controller advised the pilot to turn the airplane right to a heading of 350 degrees, which the pilot acknowledged.
> 
> Just before 0956, the controller advised the pilot to climb the airplane to 11,000 feet, which the pilot acknowledged, and at 0958, the controller advised the pilot to contact Miami Center, which the pilot also acknowledged.
> 
> The pilot then contacted Miami Center, and reported passing 6,800 feet for 11,000 feet. The controller provided the local barometric pressure, and advised the pilot of moderate to heavy precipitation along his route of flight for the next 10 miles. The pilot was given the option of deviating either left or right, and when able, to proceed direct to BAIRN.
> 
> The pilot responded "BAIRN direct when able."
> 
> At 0959:48, the controller instructed the pilot to climb the airplane to 13,000 feet, which the pilot acknowledged.
> 
> At 1001:44, the controller advised the pilot to climb and maintain 15,000 feet, but did not receive a response. After two more queries, the pilot stated that he was trying to maintain v-f-r, "I have an instrument failure here."
> 
> The controller then stated, "I'm showing you turning east. That looks like a really bad idea. If you can, turn back to the west to get out of this stuff a lot quicker, going to the west."
> 
> There were no further transmissions from the airplane.
> 
> Radar data indicated that at 1000:26, the airplane began a turn from a northerly heading approaching 90 degrees, toward the east, completing it about 1001:01. At 1001:11, the airplane reached its maximum altitude of 9,500 feet, still heading eastbound. By 1001:25, the airplane had descended to 8,100 feet, and by 1001:30, it had descended to 7,900 feet. At 1001:35, the altitude indicated 7,500 feet, and at 1001:40, the altitude indicated 0 feet (ground based altitude readouts are indicated in nearest 100-foot increments).
> 
> There was no radar indication at 1001:45, but a renewed eastbound track began with a 0-foot altitude at 1001:50, 300 feet at 1001:55, 600 feet at 1002:00, 1,100 feet at 1002:05 and 1,500 feet at 1002:10. The airplane then turned to the northeast, with the last radar contact at 1,400 feet, at 1002:15. PERSONNEL INFORMATIONThe pilot, age 75, held a commercial pilot certificate with airplane single engine land, multi-engine land and instrument airplane ratings. He also held a flight instructor certificate and was previously a U.S. Air Force pilot.
> 
> According to the pilot's logbook, as of June 1, 2013, he had 16,560 total hours of flight time, including 11,166 hours in multi-engine airplanes, 2,702 hours of actual instrument flight time and 736 hours of simulated instrument flight time. In the previous 30 days, the pilot logged 4.3 hours of actual instrument flight time and 11.3 hours of simulated instrument flight time.
> 
> The pilot's latest FAA Second Class Medical Certificate was issued on August, 21, 2012, and a review of FAA pilot medical records did not reveal any significant issues.
> 
> The pilot's wife indicated that the pilot was on a business trip, but did not know his activities the day and night before the accident or who he may have met with. The pilot's wife also stated that that she was unaware of any significant preexisting medical conditions, and that there was no pressing need for the pilot to return home that day. AIRCRAFT INFORMATIONAccording to the aircraft logbook, the latest annual inspection was completed on September 1, 2012, at an airframe time of 4,209.4 hours. At that time, both engine logbooks indicated that 100-hour inspections were completed, with both engines having 1,392.7 hours of operation since major overhaul.
> 
> The aircraft logbook also noted that, as of December 12, 2012, with no airframe hours stated, the flight director was overhauled. Other electronics items were removed for "configuration, interface and alignment with flight director. Autopilot was ground checked and a successful flight check was performed."
> 
> On January 25, 2013, at 4,230.2 hours, the left auxiliary fuel pump was removed and replaced with an overhauled pump.
> 
> The last logbook entry, on March 18, 2013, at 4,238.6 hours, "complied with visual inspection AD2001-01-16 no defects noted." According to FAA website information, that airworthiness directive applied to exhaust systems on certain Cessna 300 and 400 airplanes.
> 
> Photographs of the cockpit, taken in 2009 by a previous pilot when the airplane's registration was N226LD, showed six primary flight instruments forward of the pilot's yoke; an attitude indicator (gyro) over a horizontal situation indicator (gyro) in the center, an airspeed indicator over a turn and slip indicator to the left of those, and an altimeter over a vertical speed indicator to the right. To the right of the altimeter was the autopilot mode selector. To the right of that was a Garmin GNS 530 nav/comm and below that, a Garmin GNS 430 nav/comm. To the right of the GNS 530 was a weather radar, and to the left of the GNS 430, an Insight Strikefinder.
> 
> In front of the copilot's yoke, there was another airspeed indicator. To the right of that was another attitude gyro, and the right of that, another altimeter.
> 
> According to FAA-H-8083-25, "Pilot's Handbook of Aeronautical Knowledge," an airspeed indicator measures the difference between pitot, or impact air pressure, and static pressure. The altimeter and vertical speed indicator (rate-of-climb indicator) operate with static air only.
> 
> According to the airplane model's Pilot's Operating Handbook (POH),
> 
> The airplane had two independent pitot pressure systems, one for the pilot-side airspeed indicator, and one for the copilot-side airspeed indicator. Each system had its own pitot tube located on either side of the airplane nose cap. Heat to each pitot tube could applied via a cockpit switch.
> 
> Static pressure for the pilot-side airspeed, altimeter and rate-of-climb indicators was obtained via a normal static source aft of the main cabin door. In the event of normal static air blockage, an alternate source from within the airplane's nose compartment could have been selected by the pilot.
> 
> Copilot instruments received static pressure from a completely independent source.
> 
> The POH also noted that the proper operation of the airspeed, altimeter and rate-of-climb indicators could be determined by cross-checking the copilot instruments. In addition, "when a climb or descent is initiated, these instruments should indicate an appropriate change. If on change is indicated, it would be reasonable to assume that a static source blockage has occurred and that the alternate static source should be selected. If only the airspeed indicator appears to be affected when a climb or descent is initiated, it would be reasonable to assume that a pitot system blockage has occurred."
> 
> A vacuum system was installed to provide a source of vacuum for the vacuum instruments. The system included an engine-driven pump on each engine, a pressure relief valve for each pump, a common vacuum manifold with check valves, a vacuum air filter, and one vacuum suction gauge with failure indicator for left and right. Each vacuum pump would create a vacuum on the common manifold, exhausting the air overboard.
> 
> The POH further stated that vacuum air powered the pilot-side horizontal and directional gyros, and the copilot-side horizontal and directional gyros. If one vacuum pump failed, the manifold check valves would isolate the failed pump and the suction indication for the respective pump would move to the failed position. No corrective action was required by the pilot, as the system would automatically isolate the failed vacuum source, allowing normal operation via the remaining operative vacuum pump. METEOROLOGICAL INFORMATIONSurface weather, recorded at West Palm Beach International Airport, West Palm Beach, Florida, located about 060 degrees magnetic, 20 nm from the accident site, at 0953, included wind from 120 degrees true at 7 knots, visibility 2 statute miles, thunderstorm, heavy rain, ceiling 1,500 feet broken, 2,800 feet overcast, temperature 23 degrees C, dew point 23 degrees C, altimeter setting 30.07 inches Hg.
> 
> Ground based weather radar indicated that the airplane transitioned from an area of "green" intensity (30-35 dBZ reflectivity- light precipitation) to "yellow" (35-40 dBZ reflectivity – moderate precipitation), then "orange" (40-45 dBZ reflectivity- heavier precipitation) as it was first losing altitude. It then climbed back up into an area of "green" intensity precipitation.
> 
> Ground based weather radar also indicated that the airplane's turn to the right was toward heavier precipitation, while a straight course at that time would have initially kept the airplane in lighter precipitation.
> 
> There were no convective or non-convective Significant Meteorological Information (SIGMET) advisories active for the accident location at the accident time. There were also no Airmen's Meteorological Information (AIRMET) advisories active for the accident location at the accident time. AIRPORT INFORMATIONAccording to the aircraft logbook, the latest annual inspection was completed on September 1, 2012, at an airframe time of 4,209.4 hours. At that time, both engine logbooks indicated that 100-hour inspections were completed, with both engines having 1,392.7 hours of operation since major overhaul.
> 
> The aircraft logbook also noted that, as of December 12, 2012, with no airframe hours stated, the flight director was overhauled. Other electronics items were removed for "configuration, interface and alignment with flight director. Autopilot was ground checked and a successful flight check was performed."
> 
> On January 25, 2013, at 4,230.2 hours, the left auxiliary fuel pump was removed and replaced with an overhauled pump.
> 
> The last logbook entry, on March 18, 2013, at 4,238.6 hours, "complied with visual inspection AD2001-01-16 no defects noted." According to FAA website information, that airworthiness directive applied to exhaust systems on certain Cessna 300 and 400 airplanes.
> 
> Photographs of the cockpit, taken in 2009 by a previous pilot when the airplane's registration was N226LD, showed six primary flight instruments forward of the pilot's yoke; an attitude indicator (gyro) over a horizontal situation indicator (gyro) in the center, an airspeed indicator over a turn and slip indicator to the left of those, and an altimeter over a vertical speed indicator to the right. To the right of the altimeter was the autopilot mode selector. To the right of that was a Garmin GNS 530 nav/comm and below that, a Garmin GNS 430 nav/comm. To the right of the GNS 530 was a weather radar, and to the left of the GNS 430, an Insight Strikefinder.
> 
> In front of the copilot's yoke, there was another airspeed indicator. To the right of that was another attitude gyro, and the right of that, another altimeter.
> 
> According to FAA-H-8083-25, "Pilot's Handbook of Aeronautical Knowledge," an airspeed indicator measures the difference between pitot, or impact air pressure, and static pressure. The altimeter and vertical speed indicator (rate-of-climb indicator) operate with static air only.
> 
> According to the airplane model's Pilot's Operating Handbook (POH),
> 
> The airplane had two independent pitot pressure systems, one for the pilot-side airspeed indicator, and one for the copilot-side airspeed indicator. Each system had its own pitot tube located on either side of the airplane nose cap. Heat to each pitot tube could applied via a cockpit switch.
> 
> Static pressure for the pilot-side airspeed, altimeter and rate-of-climb indicators was obtained via a normal static source aft of the main cabin door. In the event of normal static air blockage, an alternate source from within the airplane's nose compartment could have been selected by the pilot.
> 
> Copilot instruments received static pressure from a completely independent source.
> 
> The POH also noted that the proper operation of the airspeed, altimeter and rate-of-climb indicators could be determined by cross-checking the copilot instruments. In addition, "when a climb or descent is initiated, these instruments should indicate an appropriate change. If on change is indicated, it would be reasonable to assume that a static source blockage has occurred and that the alternate static source should be selected. If only the airspeed indicator appears to be affected when a climb or descent is initiated, it would be reasonable to assume that a pitot system blockage has occurred."
> 
> A vacuum system was installed to provide a source of vacuum for the vacuum instruments. The system included an engine-driven pump on each engine, a pressure relief valve for each pump, a common vacuum manifold with check valves, a vacuum air filter, and one vacuum suction gauge with failure indicator for left and right. Each vacuum pump would create a vacuum on the common manifold, exhausting the air overboard.
> 
> The POH further stated that vacuum air powered the pilot-side horizontal and directional gyros, and the copilot-side horizontal and directional gyros. If one vacuum pump failed, the manifold check valves would isolate the failed pump and the suction indication for the respective pump would move to the failed position. No corrective action was required by the pilot, as the system would automatically isolate the failed vacuum source, allowing normal operation via the remaining operative vacuum pump. WRECKAGE AND IMPACT INFORMATIONThe wreckage was located in swampy terrain with water depths varying to about 5 feet. The initial impact point located in the vicinity of 26 degrees 30.48 minutes north latitude, 080 degrees, 24.59 minutes west longitude, or about 1,500 feet north of the last radar position. The wreckage was highly fragmented, and was dispersed along an approximately 320-degree magnetic heading. The first recognizable item at the initial impact point was the left tip tank.
> 
> The two engines were recovered, but without a propeller attached to either one. A propeller was eventually located, but was initially unrecoverable. Both engine propeller flanges were fractured, with some material missing as were some flange bolts, and other bolts were sheared off. Neither engine exhibited any evidence of pre-impact failure, nor did either vacuum pump. The cockpit vacuum pressure gauge was found frozen at 5.8 psi.
> 
> Subsequent to the departure of the investigative team, additional material, including the one propeller, was recovered. Examination of the additional wreckage occurred on November 5, 2013, with representatives from the airplane and engine manufacturers, with FAA oversight. At the time, all flight control surfaces were accounted for, but flight control continuity could only be partially confirmed due to the amount of fragmentation of the wreckage.
> 
> Pitot tubes were not observed, but a pitot tube cover was seen in a box that had been in the airplane. ADDITIONAL INFORMATIONFlight Planning
> 
> According to Lockheed Martin Flight Services (LMFS) Quality Assurance (QA), no [weather briefing] services were provided for N217JP. LMFS QA also noted that DTC (Data Transformation Corporation) DUATS (Direct User Access Terminal Service) also did not provide any services, but that CSC (Computer Sciences Corporation) did have a flight plan on file.
> 
> Air Traffic Control Services
> 
> During a recorded conversation following the accident between the "Miami Center Operations Manager in Charge" (OMIC), and an air traffic quality control group (QCG) official, the following was stated:
> 
> OMIC: "By the time he's telling him, think it's a bad idea to go to the right, the guy had already been committed going to the right to begin with and got in trouble.
> 
> QCG: "All right, so we may have led him down the garden path."
> 
> OMIC: "Yeah, by giving him that option and mentioning you can go right or left."
> 
> FAA Order JO 7110.65 "Air Traffic Control" states, in part:
> 
> "2-6-4. WEATHER…SERVICES
> 
> a. Issue pertinent information on observed/reported weather and chaff areas by defining the area of coverage in terms of azimuth (by referring to the 12-hour clock) and distance from the aircraft or by indicating the general width of the area and the area of coverage in terms of fixes or distance and direction from fixes.
> 
> Weather significant to the safety of aircraft includes such conditions as funnel cloud activity, lines of thunderstorms, embedded thunderstorms, large hail, wind shear, microbursts, moderate to extreme turbulence (including CAT), and light to severe icing.
> 
> c. Use the term 'precipitation' when describing radar-derived weather. Issue the precipitation intensity from the lowest descriptor (LIGHT) to the highest descriptor (EXTREME) when that information is available. Do not use the word 'turbulence' in describing radar-derived weather.
> 
> g. When requested by the pilot, provide radar navigational guidance and/or approve deviations around weather or chaff areas. In areas of significant weather, plan ahead and be prepared to suggest, upon pilot request, the use of alternative routes/altitudes." MEDICAL AND PATHOLOGICAL INFORMATIONAn autopsy was performed on the pilot at the District 15, State of Florida, Office of the District Medical Examiner, West Palm Beach, Florida. The cause of death was determined to be "multiple blunt traumatic injuries." Non-recovery of internal organs precluded complete examination.
> 
> Toxicological testing was performed at the FAA Forensic Toxicology Research Team, Oklahoma City, Oklahoma. No blood was available for testing. Ethanol was present in muscle and brain tissue with putrefaction (post-mortem decomposition) noted on the report.

- conclusion-term hits in factual narrative: `['the cause of']`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot’s loss of situational awareness, which resulted in an inadvertent aerodynamic stall/spin after he climbed the airplane back into instrument meteorological conditions (IMC). Contributing to the accident was the pilot’s improper decision to continue flight into IMC with malfunctioning flight instrument(s).

- duplicate stripped finding descriptions in this event: **0**

---

## 4. `20100624X25616` — CEN10CA341

- date: `06/22/10 00:00:00`  year `2010`  type `ACC`
- location: Albuquerque, NM USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Action/decision-Action-Forgotten action/omission-Pilot | `C` | `0204103544` |
| 1 | 2 | `F` | `T` | Personnel issues-Task performance-Workload management-(general)-Pilot | `F` | `0206400044` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 157 words

> According to the pilot's accident report, during the initial climb from Albuquerque Sunport (ABQ), New Mexico, he noticed the airspeed indicator was erratic and not indicating a normal climb speed. After leveling off, the indicated airspeed was 70 to 80 knots. He compared this with the GPS (Global Positioning System) ground speed and noticed a "significant difference." Later, while circling a house, the airspeed "went to zero knots." The pilot returned for landing at ABQ. He said he mentally went through the GUMPs (gas, undercarriage, mixture prop) checklist but was distracted by the airspeed indicator and radio traffic. As he flared for landing and reduced power, he heard a horn sounding and mistook it for the marker beacon alert. The airplane landed wheels up. A post-accident examination revealed the airplane's fuselage skin and U-shaped former (where the lift struts attach) were ground down, necessitating replacement. An examination of the pitot tube showed it was plugged with insects.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's failure to lower the landing gear. Contributing to the accident was the pilot's distraction with an erroneous airspeed indicator.

- duplicate stripped finding descriptions in this event: **0**

---

## 5. `20120825X85310` — CEN12FA570

- date: `08/25/12 00:00:00`  year `2012`  type `ACC`
- location: Llano, TX USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Task performance-(general)-(general)-Instructor/check pilot | `C` | `0206000040` |
| 1 | 2 | `F` | `T` | Personnel issues-Physical-Impairment/incapacitation-OTC medication-Instructor/check pilot | `F` | `0201203040` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 1819 words

> HISTORY OF FLIGHT
> 
> On August 25, 2012, about 1045 central daylight time, an American AA-1 airplane, N5796L, impacted terrain near Llano, Texas. The flight instructor and student pilot were fatally injured. The airplane was substantially damaged during the accident. The aircraft was registered to and operated by a private individual under the provisions of 14 Code of Federal Regulations Part 91 as an instructional flight. Visual meteorological conditions prevailed for the flight, which operated without a flight plan.  The flight originated from the Llano Municipal Airport, (KAQO). 
> 
> The airport manager reported that he saw the student, who owned the airplane, pull the airplane from the hangar and add fuel.  The manager also saw the student and instructor depart the runway, but stay in traffic pattern practicing takeoff and landings.  The manager also reported that he told the instructor, via the radio, that a jet was scheduled around 1100 inbound to the airport.  The instructor acknowledged the transmission.  There was no additional communication with the accident airplane.  The manager added that he thought the student and instructor had departed the traffic pattern and was not concerned until about 1400, when the instructor’s next student showed up.
> 
> After the airport manager contacted several nearby airports  and could not locate the airplane,  a local pilot departed the airport to search for the airplane.  Within a few minutes the pilot reported that he had spotted the missing airplane’s wreckage, southeast of the runway. 
> 
> The wreckage was located in a lightly wooded area with cactus plants, approximately one mile southeast of the airport.
> 
> A witness, reported he was flying a helicopter on the day of the accident and approached the Llano airport about 1045. He noted that there were several airplanes in the traffic pattern and he saw a flash of a wing and an airplane quickly departed controlled flight towards the ground.   He added that he flew near the area and since he didn’t see any wreckage, dismissed the sighting as someone flying a radio controlled ( RC) airplane. 
> 
> An additional witness reported that he and several other people were working near the airfield between 1000 and 1200.   He stated that he saw an airplane on the downwind leg of the traffic pattern, but what was unusual, was that the airplane was operating at a very high angle-of-attack.  He added, that a few minutes later he observed the airplane, in the same location, operating in the same manner.
> 
> PERSONNEL INFORMATION 
> 
> The flight instructor held commercial pilot certificates for airplane, single and multi-engine land, and instrument airplane.   He also held flight instructor ratings for single, multi-engine and instrument airplane.  A second-class Federal Aviation Administration (FAA) medical was issued on August 31, 2011 with the restriction that he must wear corrective lenses.  The instructor’s logbook was not provided; however, the instructor reported on his last medical certificate he had accumulated 8,577 total flight hours with 783 hours in the last six months. 
> 
> The student pilot did not hold a student pilot or medical certificate.  A review of FAA records revealed that the student applied for a medical certificate on August 17, 2012; however, the certificate was not issued pending additional information.  At the time of the application, the student pilot reported a total of 15 flight hours with 15 hours in the last six months.  A review of the student pilot’s logbook revealed that he had a total of 14.7 flight hours, with 12.5 hours in the accident airplane; the last recorded entry was on August 24, 2012.  A detailed review of the student’s logbook revealed that he had two flights in February and one in March with a different instructor, as well as a different make/model of airplane then the accident airplane.   Starting on June 29, 2012, the student pilot and accident flight instructor flew the accident airplane on a weekly basis.  The June 29th flight was recorded as a 1.0 hour flight with the annotation of:  “orientation flight Grumman”.  The student pilot logbook’s last five entries were annotated as; patterns, touch-and-goes and there were no records of any stall or spin avoidance training noted in his logbook.
> 
> 
> AIRCRAFT INFORMATION
> 
> The accident airplane was an American AA-1 airplane, which is an all-metal, side-by-side, two-seat low-wing airplane with fixed landing gear.  The accident airplane was a 1969 model; according to FAA records, the student pilot purchased the airplane in April, 2012.  The airplane was powered by a 108hp Lycoming O-235-C2C engine, that drove a fixed-pitch, two-bladed, metal propeller.
> According to maintenance records, the airplane's most recent annual inspection was completed June 26, 2012, with an airframe total time of 1,683.01 hours and tachometer time of 873.01 hours.   The review of the maintenance records also revealed that a note annotated in the logs read; “Removed, inspected, and tested ELT, IAW FAR 91.207(d) no defects noted, new ELT battery due date is 5-14”.
> 
> 
> METEOROLOGICAL INFORMATION
> 
> At 1055, the automated weather observation facility located at KAQO,  recorded wind from 190 degrees at 13 knots, gusting to 16 knots, visibility 10 miles, clear of clouds, temperature 86 degrees Fahrenheit (F), dew point 44 F, and a barometric pressure of 29.95 inches of mercury.
> 
> A review of the carburetor icing probability chart, located in the FAA's Special Airworthiness Information Bulletin CE-09-35, dated June 30, 2009, and relevant meteorological data, revealed that the weather conditions for carburetor icing were favorable for serious icing at glide power.
> 
> 
> AIRPORT INFORMATION
> 
> Llano Municipal Airport (KAQO), is a public use airport, located about 2 miles northeast of Llano, Texas. The airport is non-towered and pilots are to use the Common Traffic Advisory Frequency (CTAF). The airport features an asphalt runway, 17-35 which is 4,202-foot long and 75-foot wide and a turf runway, 13-31 which is 3,209-foot long and 150-foot wide.
> 
> 
> 
> 
> 
> COMMUNICATIONS 
> 
> The pilot was not in contact with air traffic control and there were no reported distress calls from the pilot.  
> 
> 
> WRECKAGE AND IMPACT INFORMATION 
> 
> The National Transportation Safety Board, inspectors from the Federal Aviation Administration (FAA), and a technical representative from the engine manufacturer examined the airplane wreckage on site. 
> 
> The impact area was between trees and covered with small bushes and cacti.   Two ground impact scars were located just in front of the wreckage.  The engine and front fuselage sections displayed extensive crushing.  Both wings remained with the wreckage, but the wing spar was broken at the wing root on the left and right side of the fuselage.  Both wings had extensive buckling and dents over their entire area. Just a short distance from the wreckage, on the other side of a wire fence, was an open, grass field.  The airplane wreckage and ground scars were consistent with a steep nose down collision with terrain.  
> 
> The airplane’s left and right wing fuel tanks, which was also the main wing spar, had been breached and absent of fuel; vegetation blight and fuel odor was not detected on-site.
> 
> The propeller remained bolted to the engine crankshaft; one blade had only a slight bend. The blade’s black and white painted tip remained and the blade was absent any leading edge gouges or polishing.  The remaining blade was bent back, towards the cambered side, about mid-span, at an estimated 45-degree angle, the blade’s paint had widespread scratches and was polished off near the bend.  The engine starter, located behind the propeller and crankshaft ring gear, had an impact mark, but was absent rotational scoring.
> 
> The empennage exhibited only minor damage to the horizontal, vertical stabilizers, and their respective control surfaces.  The rudder, elevator and trim tab, remained attached via their respective hinges.  The airplane’s emergency locator transmitter (ELT) was located in the empennage section; the unit’s activation switch was found in the “off” position.
> 
> 
> 
> MEDICAL AND PATHOLOGICAL INFORMATION
> 
> The Travis County Medical Examiner’s Office, Austin, Texas, Office of the Medical Examiner, conducted autopsies on the flight instructor and student pilot.  The causes of death, in both cases, were determined to be, “blunt force injuries”.
> 
> The FAA Toxicology Accident Research Library, Oklahoma City, Oklahoma, conducted toxicological testing on the flight instructor.  The results were negative for carbon monoxide, cyanide, and ethanol.  Diphenhydramine was detected in the liver and in cavity blood at 0.051ug/ml.  Diphenhydramine is a sedating antihistamine and sleep aid available over the counter in drugs marketed under the trade names Benadryl, Unisom, and Sominex.
> 
> The FAA Toxicology Accident Research Library, Oklahoma City, Oklahoma, conducted toxicological testing on the student pilot.  The results were negative for carbon monoxide, cyanide, and ethanol. Alpha-hydroxyalprazolam was detected in urine, but not in the blood and its parent molecule alprazolam was not identified in either.  Alprazolam is a benzodiazepine anxiolytic prescribed as a Schedule IV controlled substance and marketed under the trade name Xanax.  Alpha-hydroxyalprazolam is a biologically active primary metabolite of alprazolam.  
> 
> 
> TEST AND RESEARCH
> 
> Control continuity was established from each of the respective control surfaces to the cabin section of the fuselage.
> 
> The airplane’s stall warning switch, located in the leading edge of the wing was removed. A multimeter was used to check electrical continuity.  When the switch was activated, no continuity was observed.  The electrical screws used to connect the wiring to the switch were removed. A small amount of corrosion was observed under the terminal ends of the wires and switch contact points.  The wiring and screws were reassembled and the test was repeated; when activated, electrical continuity was noticed on the meter. A mechanic’s work order dated, August 3, 2013, contained the annotation:  adjusted stall warning.  A family member reported that the student pilot (and airplane owner) stated to family members a couple days before the accident that “the stall warning still was not working right” and that the flight instructor would disable it for each flight.
> 
> The aircraft engine sustained heavy impact damage.  Continuity from the propeller through the crankshaft and pistons, camshaft, and valve train was established.   A thumb compression test was performed on each cylinder. The two magnetos had separated from the engine; damage to the magnetos prevented testing of the magnetos.  The engine drive fuel pump was broken, but appeared free to move. The rocker covers were removed and the valves were able to move, when the engine was rotated.
> 
> The carburetor received impact damage and had broken at the throttle plate.  The carburetor’s fuel inlet screen was absent any debris or contaminates. The float bowel was opened and only residual fuel remained in the bowl, the floats were free to move, unmarked and were not damaged.  A water detecting paste was used on the fuel in the carburetor bowl; the test was negative for water.
> 
> The sparkplugs were removed; generally displayed light, grey deposits and were consistent with normal combustion and operation. 
> 
> ADDITIONAL INFORMATION
> FAA-H-8083-3A, Airplane Flying Handbook
> In the absence of the manufacturer’s recommended spin recovery procedures and techniques, the following spin recovery procedures are recommended.
> 
> Step 1—REDUCE THE POWER (THROTTLE) TO IDLE. 
> Power aggravates the spin characteristics. It usually results in a flatter spin attitude and increased rotation rates.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The flight instructor’s delayed remedial action and inadequate supervision during practice traffic pattern work.  Contributing to the accident was the flight instructor’s use of sedating medication on the day of the accident and airplane’s high angle of attack at a low altitude during the traffic pattern turn, which prevented recovery during an aerodynamic stall.

- duplicate stripped finding descriptions in this event: **0**

---

## 6. `20151201X31241` — ANC16CA009

- date: `11/27/15 00:00:00`  year `2015`  type `ACC`
- location: Manley Hot Springs, AK USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Action/decision-Info processing/decision-Decision making/judgment-Pilot | `C` | `0204152044` |
| 1 | 2 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 3 | `F` | `T` | Environmental issues-Physical environment-Runway/land/takeoff/taxi surface-Snow/slush/ice covered-Effect on equipment | `F` | `0302301581` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 83 words

> The pilot reported that prior to departing in a ski-equipped airplane, from a remote frozen, snow covered lake; he prepared the off-airport site by packing down the loose snow. During his takeoff roll, the left ski slid off the prepared surface, and encountered loose snow and water overflow which pulled the airplane hard to the left. The left wing struck a tree, substantially damaging the left wing. The pilot stated that there were no preaccident mechanical anomalies that would have precluded normal operation.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's decision to depart from an unsuitable, off-airport site, which resulted in a collision with a tree.

- duplicate stripped finding descriptions in this event: **0**

---

## 7. `20080703X00979` — SEA08CA151

- date: `06/17/08 00:00:00`  year `2008`  type `ACC`
- location: Point Roberts, WA USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `F` | `T` | Environmental issues-Conditions/weather/phenomena-Wind-Tailwind-Contributed to outcome | `F` | `0303401591` |
| 1 | 2 | `-` | `F` | Environmental issues-Physical environment-Object/animal/substance-Tree(s)-Not specified | `-` | `0302202099` |
| 1 | 3 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Altitude-Not attained/maintained | `C` | `0106201220` |
| 1 | 4 | `F` | `T` | Personnel issues-Action/decision-Action-Delayed action-Pilot | `F` | `0204102544` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 108 words

> While attempting a landing in visual meteorological conditions, the pilot inadvertently allowed the airplane to porpoise during the landing flare. He therefore initiated a go-around, but did not clear some trees about one-quarter mile off the departure end of the runway. After impacting the trees, he was able to maintain airplane control, and subsequently executed a second approach and a full-stop landing. After the landing, the pilot realized that his first approach had been made with a tailwind of about 20 knots. The impact with the tress resulted in numerous dents in the leading edge of the wings, and a tear in the skin of the horizontal stabilizer.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's failure to maintain clearance from trees during a go-around. Contributing to the accident were the pilot inadvertently allowing the airplane to porpoise during the landing flare, and the presence of a tailwind.

- duplicate stripped finding descriptions in this event: **0**

---

## 8. `20120704X95425` — ERA12LA429

- date: `07/04/12 00:00:00`  year `2012`  type `ACC`
- location: Tallahassee, FL USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Altitude-Not attained/maintained | `C` | `0106201220` |
| 1 | 2 | `C` | `T` | Personnel issues-Action/decision-Info processing/decision-Identification/recognition-Pilot | `C` | `0204151044` |
| 1 | 3 | `F` | `T` | Personnel issues-Physical-Alertness/Fatigue-(general)-Pilot | `F` | `0201350044` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 932 words

> On July 4, 2012, approximately 0340 eastern daylight time, a Robinson R44 helicopter, N561CH, was substantially damaged when it impacted a lake while maneuvering near Tallahassee, Florida. The certificated private pilot was not injured. Night visual meteorological conditions prevailed, and no flight plan was filed for the flight, which departed Tallahassee Regional Airport (TLH), Tallahassee, Florida, about 0330. The personal flight was conducted under the provisions of Title 14 Code of Federal Regulations Part 91. 
> 
> The pilot stated that he had woken up at 0900 the morning of July 3, and he and another pilot had driven approximately six hours to West Palm Beach, Florida, to pick up a helicopter and fly it back to TLH. The flight from West Palm Beach to TLH was conducted from about 2230 – 0200. Upon arriving at TLH, the pilot decided to take the accident helicopter on a short flight to build night flight time and conduct a landing in order to meet night proficiency requirements. After departing TLH, he followed a road to the northeast at an altitude between 600-800 feet mean sea level for about 8 minutes, before turning back towards TLH. The turn was conducted over the pilot’s residence, which was located next to a lake.
> 
> During the turn, the pilot saw the clutch actuator light illuminate and remain illuminated for 9 seconds. The pilot reached for the circuit breaker box under the passenger seat to pull the clutch circuit breaker, and then felt "light in the seat." He stated that the helicopter was rapidly descending, and he increased collective pitch to arrest the descent. After increasing collective pitch, he heard the low rotor rpm horn sound and then observed the surface of the lake reflecting the moonlight about 50 feet below the helicopter, as it continued to descend. The pilot increased collective pitch to soften the impact and the helicopter came to rest in the lake. The pilot then egressed the helicopter and swam to shore. 
> 
> The helicopter was recovered from the lake on July 7, 2012 and moved to a secure location for further examination. 
> 
> According to FAA records, the helicopter was manufactured in 2008, and was equipped with a Lycoming O-540, 260 hp, reciprocating engine. According to maintenance records, its most recent 100-hour inspection was completed on May 29, 2012 at a total time of 1298.6 hours. At the time of the accident, the helicopter had accumulated 1,336 total hours. 
> 
> The pilot held a private pilot certificate with a rating for rotorcraft-helicopter, which was issued in March, 2012. He reported a total flight time of 204 hours, of which 181 hours were in the accident helicopter make and model, and 11 hours were at night. His most recent FAA second-class medical certificate was issued in April, 2012. 
> 
> The helicopter was examined on August 17, 2012. Control continuity was established from the cyclic and collective controls in the cockpit to the main rotor. Flight control and drive train continuity were confirmed from the anti-torque pedals to tail rotor gearbox through a fracture of the tail boom. 
> 
> The four v-belts were found in place on the sheave and were observed to be taut and in good condition. The v-belts and clutch actuator were removed and sent to the manufacturer, where they were examined on August 23, 2012. 
> 
> Visual inspection revealed no damage or unusual wear on any of the four v-belts. The clutch actuator was observed to be extended approximately one inch.
> 
> After freeing the motor to rotate using hand pressure, the actuator was installed on a production test fixture, and operated normally in both directions. The down-limit switch functioned correctly, and subsequently shut off the motor when the down (belt-loosening) limit was reached. In the up, or belt-tensioning, direction, both spring switches activated simultaneously as designed. The actuator was cycled an additional two times and operated with no anomalies.
> 
> The 0353 weather observation at TLH included winds from 190 degrees at 3 knots, 10 miles visibility, clear skies, temperature 23 degrees C, dew point 21 degrees C, and an altimeter setting of 30.00 inches of mercury. According to U.S. Naval Observatory Astronomical data for the morning of the accident, the moon rose at 2042 on July 3, and set at 0735 the morning of July 4. The moon's phase was a waning gibbous with 99% of its visible disk illuminated.
> 
> The Robinson R44 Pilot’s Operating Handbook stated regarding the clutch actuator light: “CLUTCH – indicates that clutch actuator is on, either engaging or disengaging the clutch. When the switch is in the ENGAGE position, the light stays on until the belts are properly tensioned…NOTE: The clutch light may come on momentarily during run-up or during flight to retension the belts as they warm-up and stretch slightly. This is normal. If, however, the light flickers or comes on in flight and does not go out within 7 to 8 seconds, pull the CLUTCH circuit breaker, reduce power, and land immediately. Be prepared to enter autorotation. Inspect drive system for a possible malfunction.” 
> 
> According to FAA Advisory Circular AC120-100, “Basics of Aviation Fatigue,” a window of circadian low normally occurs between 3 a.m. and 5 a.m. This is a period of low alertness and performance and elevated operational risk. AC120-100 further states that, in many work environments, a large increase in error rates and accident likelihood occurs in the early morning hours between 2 a.m. and 4 a.m. that roughly coincides with the minimum of the circadian rhythm of core body temperature.
> 
> The helicopter was recovered from the lake on July 7, 2012 and moved to a secure location pending further examination.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot’s failure to maintain awareness of the helicopter’s altitude while attempting to troubleshoot the clutch actuator warning light, which resulted in an inadvertent descent and impact with water. Contributing to the accident was the pilot's possible fatigue.

- duplicate stripped finding descriptions in this event: **0**

---

## 9. `20140408X72606` — ERA14CA185

- date: `04/08/14 00:00:00`  year `2014`  type `ACC`
- location: Leesburg, VA USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Directional control-Not attained/maintained | `C` | `0106202020` |
| 1 | 2 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 3 | `C` | `T` | Environmental issues-Conditions/weather/phenomena-Wind-Gusts-Response/compensation | `C` | `0303404585` |
| 1 | 4 | `F` | `T` | Personnel issues-Action/decision-Info processing/decision-Identification/recognition-Pilot | `F` | `0204151044` |
| 1 | 5 | `-` | `F` | Environmental issues-Operating environment-Meteorological services-Meteo equip coverage/avail-Availability of related info | `-` | `0301301088` |
| 1 | 6 | `-` | `F` | Environmental issues-Physical environment-Terrain-(general)-Contributed to outcome | `-` | `0302100091` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 284 words

> According to the pilot's origination airport, which was 21 nautical miles from the destination airport, there was a 6 knot wind when he departed. The pilot flew west and encountered turbulence after clearing the Washington D.C. Special Flight Rules Area. Twenty five minutes into the flight, the pilot discovered that his destination airport, which was several miles away, was not reporting wind. Expecting wind similar to what he experienced at his originating airport, the pilot proceeded to the destination airport and entered the traffic pattern on the downwind leg. In order to maintain his course he entered a crab angle. The pilot turned to the base leg of the traffic pattern and then established himself on final approach where he observed about a 12 knot wind indication from the windsock. He maneuvered the airplane into a left wing low attitude with full right rudder in order to line up with the centerline of runway 35. Once over the runway, the pilot flared the airplane nose; however, a strong wind gust pushed it to the right. He applied full power to initiate a go around maneuver, but the wind continued to carry the airplane to the right. The left main landing gear touched down in "soggy" grass terrain and the nose landing gear subsequently impacted the ground. The airplane then nosed over and came to rest inverted. Postaccident examination of the wreckage revealed substantial damage to the engine firewall, fuselage, and left wing. The pilot reported no mechanical malfunctions or anomalies with the airframe or engine that would have precluded normal operation.
> 
> At the time of the accident, the wind at Washington-Dulles International Airport was reported from 300 at 19 knots gusting to 32 knots.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's inadequate compensation for the wind conditions during landing, resulting in a runway excursion and impact with terrain. Contributing to the accident was the pilot's inadequate evaluation of the wind conditions.

- duplicate stripped finding descriptions in this event: **0**

---

## 10. `20171123X70738` — ERA18FA030

- date: `11/23/17 00:00:00`  year `2017`  type `ACC`
- location: Starke, FL USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 2 | `C` | `T` | Personnel issues-Psychological-Perception/orientation/illusion-Spatial disorientation-Pilot | `C` | `0202202544` |
| 1 | 3 | `C` | `T` | Environmental issues-Conditions/weather/phenomena-Ceiling/visibility/precip-Rain-Effect on operation | `C` | `0303503582` |
| 1 | 4 | `C` | `T` | Environmental issues-Conditions/weather/phenomena-Ceiling/visibility/precip-Clouds-Effect on operation | `C` | `0303502582` |
| 1 | 5 | `C` | `T` | Environmental issues-Conditions/weather/phenomena-Turbulence-(general)-Effect on operation | `C` | `0303200082` |
| 1 | 6 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-(general)-Not attained/maintained | `C` | `0106200020` |
| 1 | 7 | `F` | `T` | Personnel issues-Experience/knowledge-Experience/qualifications-Recent experience-Pilot | `F` | `0203103544` |
| 1 | 8 | `F` | `T` | Personnel issues-Psychological-Personality/attitude-Motivation/respond to pressure-Pilot | `F` | `0202102544` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 2402 words

> HISTORY OF FLIGHTOn November 23, 2017, about 1515 eastern standard time, a Mooney M20, N6894N, was destroyed when it impacted terrain near Starke, Florida. The private pilot was fatally injured. The airplane was privately owned and operated as a Title 14 Code of Federal Regulations (CFR) Part 91 personal flight. Instrument meteorological conditions prevailed at the time and an instrument flight rules (IFR) flight plan was filed for the flight, which originated about 1419 from Ocala International Airport-Jim Taylor Field (OCF), Ocala, Florida, with a destination of Cecil Airport (VQQ), Jacksonville, Florida.
> 
> A friend of the pilot reported that she flew to OCF as a passenger with the accident pilot in the accident airplane earlier on the day of the accident. She said that the flight was uneventful until they approached OCF, when the weather became "very turbulent." The pilot mentioned to her that he was trying to maintain altitude as he was preparing for landing. She said that, after they landed, it was "very windy and raining very hard." They went inside the fixed-base-operator (FBO), where the pilot mentioned that he had to get to VQQ for his daughter's birthday and Thanksgiving. She told him that he should "wait it out," and he agreed.
> 
> FBO personnel reported that, as the pilot waited for the weather to improve, he asked them to top off the airplane's fuel tanks. They advised the pilot that the weather was very bad and that he should wait for the fuel. The pilot said that he needed the fuel "now" because he was trying to get to his daughter's house for Thanksgiving and requested that the line personnel wipe his fuel caps with a towel and use an umbrella to prevent rainwater from entering the fuel tanks. After about 45 minutes, the pilot said that he was "heading out"; when asked if he found a break in the weather, the pilot laughed and said he was "gonna go for it."
> 
> Review of air traffic control radar and voice communication information from the Federal Aviation Administration (FAA) Jacksonville Air Route Traffic Control Center (JAX ARTCC) revealed that, as the pilot departed OCF he was advised to "climb and maintain three thousand." The JAX ARTCC approach controller identified the pilot's airplane, instructed him to proceed direct to VQQ, advise when he had the ATIS, and expect the "ILS to RWY36R." The controller then cleared the airplane direct to "NOLFO" the initial approach fix for the runway 36R instrument landing system (ILS) approach. The pilot asked the controller to spell out the intersection which the controller did, and the controller subsequently informed the pilot "your uh target's going all over the place you having issues." The pilot attributed the airplane's motion as described by the controller as due to wind and further indicated that he was not having any issues.
> 
> The JAX ARTCC approach controller asked the pilot if he wanted to try a different altitude, but the pilot declined and responded "…i'm okay."
> 
> The airplane was cleared for the ILS approach to runway 36R at 1455:47 and the pilot was instructed to maintain 3,000 ft until reaching NOLFO; however, the pilot read back 2,000 ft and was corrected by the approach controller. At 1459:26, the pilot was instructed to contact the VQQ air traffic control tower (ATCT), which the pilot did not acknowledge until the instruction was repeated by the controller.
> 
> At 1501:19, the JAX ARTCC approach controller provided a low altitude alert to the VQQ tower controller. The approach controller noted that the airplane was "going back and forth on the localizer" and asked the VQQ ATCT controller if he was able to see the airplane. The VQQ ATCT controller said he could not see the airplane due to the low ceilings. About 2002, the VQQ tower controller advised the JAX ARTCC controller that the pilot was coming back to JAX ARTCC approach, and the pilot was subsequently provided radar vectors for a second  ILS to runway 36R.
> 
> While JAX ARTCC approach controller was providing the pilot radar vectors, he noted that the airplane was triggering low altitude alarms. At 1511:02, when the pilot was asked if he was able to climb and turn, the pilot indicated that he could but needed to go out for a long approach. At 1513:02, the controller asked the pilot if he would like to land at Jacksonville International Airport (JAX), Jacksonville, Florida, which was reporting higher ceilings and better visibility. The pilot elected fly to JAX and was provided initial and repeated vectors. The pilot initially acknowledged the heading but did not acknowledge the altitude assignment. Shortly thereafter, at 1515, radar contact with the airplane was lost.
> 
> An alert notice (ALNOT) was subsequently issued and the airplane was located at 1600 in a field about 18 nautical miles south-southwest of VQQ. PERSONNEL INFORMATIONThe pilot, age 73, held a private pilot certificate with ratings for airplane single-engine land and instrument airplane. He also held an FAA third-class medical certificate, issued July 11, 2016. A review of the pilot's logbook revealed 3,146 total hours of flight experience; the most recent entry was dated September 8, 2017. The pilot had accumulated 400 flight hours in the accident airplane make and model, and 4 hours within the previous 90 days. The pilot recorded a total of 527 actual instrument hours; since January 1, 2016, he had flown 18 actual instrument flight hours, 8 of which were in 2017. A review of the pilot's logbook revealed that he did not meet FAA recency requirements to act as pilot in command under IFR or weather conditions less than the minimums prescribed for visual flight rules. AIRCRAFT INFORMATIONThe single-engine airplane was manufactured in 1968 and was powered by a Lycoming O-360-A1D engine rated at 180 horsepower, equipped with a Hartzell three-bladed, controllable-pitch propeller. The most recent annual inspection was completed on August 1, 2017, at a tachometer time of 2,895.49 hours. At the time of the accident, the tachometer reading was 2,911.22 hours. The Hobbs meter was destroyed during the accident, and the current airframe total times could not be determined. A review of the maintenance logbooks revealed that the last altimeter/pitot-static system and transponder test was performed on June 15, 2015. METEOROLOGICAL INFORMATIONVQQ was located about 18 miles north-northeast of the accident site at an elevation of 80 ft. The recorded VQQ special weather observation at 1511 included wind from 030° at 12 knots, 2 miles visibility in mist, overcast ceiling at 900 ft above ground level (agl), temperature and dew point 17°C, and altimeter setting of 29.87 inches of mercury (inHg).
> 
> The closest weather reporting location was Keystone Airpark (42J) Keystone Heights, Florida, located about 8 miles south-southwest of the accident site. The 1515 recorded observation at 42J included wind from 040° at 8 knots, 10 miles visibility or more, broken ceiling at 800 ft agl, overcast ceiling at 1,100 ft agl, temperature and dew point 18°C, and altimeter setting of 29.85 inHg.
> 
> Weather Surveillance Radar
> 
> The National Weather Service KJAX WSR-88D detected a large area of light to moderate intensity echoes along the airplane's flight track and in the vicinity of the accident site, and indicated that the accident flight was in clouds and precipitation when the flight deviated west and then back to the south. The 1513 base reflectively image showed that the airplane's flight track operated through echoes of 30 to 40 dBZ, moderate intensity echoes and in an area of 15 to 20 dBZ echoes at the time of the accident (See figure 1).
> 
> 
> 
> 
> 
> Figure 1. KJAX WSR-88D 0.5° base reflectivity image for 1513 with airplane's flight track of overlaid
> 
> 
> 
> Preflight Weather Briefing
> 
> The pilot filed IFR flight plans at 0858 and at 1405 with Leidos Flight Service; however, the pilot did not request any weather briefings. There was no record of contact with any other Direct User Access Terminal Service (DUATS) providers or with ForeFlight; therefore, what weather products or advisories the pilot may have familiarized himself with before the flight could not be determined. AIRPORT INFORMATIONThe single-engine airplane was manufactured in 1968 and was powered by a Lycoming O-360-A1D engine rated at 180 horsepower, equipped with a Hartzell three-bladed, controllable-pitch propeller. The most recent annual inspection was completed on August 1, 2017, at a tachometer time of 2,895.49 hours. At the time of the accident, the tachometer reading was 2,911.22 hours. The Hobbs meter was destroyed during the accident, and the current airframe total times could not be determined. A review of the maintenance logbooks revealed that the last altimeter/pitot-static system and transponder test was performed on June 15, 2015. WRECKAGE AND IMPACT INFORMATIONThe wreckage came to rest on a 314° heading about 18 miles from VQQ on the training base of Camp Blanding Military Reservation, Florida. The fuselage was broken into two parts; the cockpit and empennage separated aft of the rear seat at the wing spars. All flight control surfaces were located at the accident site along the debris path.
> 
> All flight controls were destroyed and their respective control tubes were impact damaged. Continuity of the flight control tubes could not be established, but the tubes from the yoke mounts to the wing roots were present. Engine and propeller controls were impact damaged and did not reveal useful information. The fuel selector was noted in the left wing tank position and 10 gallons of liquid consistent with aviation fuel was drained from the left wing tank. Flight control tubes in the left wing were attached to the left aileron and the aileron remained attached to the wing surface. The flap remained attached to the wing and the flap control tubes were damaged. The position of the flaps at the time of impact could not be established. The right wing was fragmented along the debris path; its associated flight controls were accounted for and impact damaged.
> 
> The empennage was buckled; both horizontal stabilizers and elevators remained attached. The elevator control tubes remained attached to the elevators but  were broken within the fuselage. The vertical stabilizer was separated and located along the debris path. The rudder was separated from the vertical stabilizer and located along the debris path. The rudder and elevator control tubes were located within the empennage and buckled but could not be manipulated due to impact damage.
> 
> The engine was impact-damaged. The engine was partially dissembled for examination and the engine accessories were removed. Rotation of the crankshaft produced thumb compression and valve train movement on all four cylinders. The spark plugs were removed and were gray. The oil sump screen was removed and was free of debris. Both magnetos were impact-damaged. The ignition leads were broken and separated from the spark plugs. The magneto drive gear was rotated on both magnetos and produced spark on all ignition leads. The vacuum pump was disassembled and all internal vanes were intact. The internal drive coupling was intact and not damaged. The carburetor was separated from the engine and impact damaged. The carburetor was disassembled and the bowl was free of debris. Examination of the fuel screen revealed insignificant amounts of debris. The throttle and mixture cable were separated from the carburetor and impact damaged.
> 
> All three propeller blades were damaged and remained attached to the hub; the hub remained attached to the crankshaft. One blade was bent aft and had chordwise scoring, one blade remained relatively straight with scoring, and one blade exhibited "S" bending and scoring along its span.
> 
> No anomalies of the airframe and engine were noted that would have precluded normal operation. ADDITIONAL INFORMATIONAccording to the FAA's General Aviation Joint Steering Committee, a pilot's sight, supported by other senses, allows a pilot to maintain orientation while flying. However, when visibility is restricted (i.e., no visual reference to the horizon or surface detected), the body's supporting senses can conflict with what is seen. When this spatial disorientation occurs, sensory conflicts and optical illusions often make it difficult for a pilot to tell which way is up.
> 
> The FAA Airplane Flying Handbook (FAA-H-8083-3) describes some hazards associated with flying when visual references, such as the ground or horizon, are obscured. The handbook states:
> 
> The vestibular sense (motion sensing by the inner ear) in particular tends to confuse the pilot. Because of inertia, the sensory areas of the inner ear cannot detect slight changes in the attitude of the airplane, nor can they accurately sense attitude changes that occur at a uniform rate over a period of time. On the other hand, false sensations are often generated; leading the pilot to believe the attitude of the airplane has changed when in fact, it has not. These false sensations result in the pilot experiencing spatial disorientation.
> 
> FAA AC-00-6B, Aviation Weather, describes thunderstorms and the turbulence that is associated with them. The AC stated, in part:
> 
> Turbulence is present in all thunderstorms. Severe or extreme turbulence is common. Gust loads can be severe enough to stall an aircraft at maneuvering speed or to cause structural damage at cruising speed. The strongest turbulence occurs with shear between updrafts and downdrafts. Outside the cumulonimbus cloud, turbulence has been encountered several thousand feet above, and 20 miles laterally from, a severe storm.
> 
> The Turbulence Reporting Criteria Table in the FAA Aeronautical Information Manual provides the following definitions:
> 
> Severe: Turbulence that causes large, abrupt changes in altitude and/or attitude. It usually causes large variations in indicated airspeed. Aircraft may be momentarily out of control.
> Extreme: Turbulence in which the aircraft is violently tossed about and is practically impossible to control. It may cause structural damage.
> 
> FAA Advisory Circular AC 60-22, Aeronautical Decision Making, stated, "Pilots, particularly those with considerable experience, as a rule always try to complete a flight as planned, please passengers, meet schedules, and generally demonstrate that they have 'the right stuff.'" One of the common behavioral traps identified was "Get-there-itis." The text stated, "Common among pilots, [get-there-itis] clouds the vision and impairs judgment by causing a fixation on the original goal or destination combined with a total disregard for any alternative course of action." MEDICAL AND PATHOLOGICAL INFORMATIONThe Office of the Medical Examiner, Jacksonville, Florida, performed an autopsy on the pilot. The cause of death was noted as multiple blunt force trauma.
> 
> Toxicology testing performed by the FAA's Bioaeronautical Sciences Research Laboratory was negative for carbon monoxide, cyanide, basic, acidic, and neutral drugs with the exception of:
> 
> Salicylates (i.e. aspirin) which was detected in urine was previously reported by the airman.

- conclusion-term hits in factual narrative: `['the cause of']`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's loss of control due to spatial disorientation while maneuvering in instrument meteorological conditions. Contributing was the pilot's lack of instrument currency and his self-induced pressure to complete the flight.

- duplicate stripped finding descriptions in this event: **0**

---

## 11. `20180416X75158` — ERA18FA127

- date: `04/16/18 00:00:00`  year `2018`  type `ACC`
- location: Crozet, VA USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 2 | `C` | `T` | Personnel issues-Psychological-Perception/orientation/illusion-Spatial disorientation-Pilot | `C` | `0202202544` |
| 1 | 3 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-(general)-Not attained/maintained | `C` | `0106200020` |
| 1 | 4 | `F` | `T` | Personnel issues-Action/decision-Info processing/decision-Decision making/judgment-Pilot | `F` | `0204152044` |
| 1 | 5 | `F` | `T` | Personnel issues-Physical-Impairment/incapacitation-Alcohol-Pilot | `F` | `0201201544` |
| 1 | 6 | `C` | `T` | Environmental issues-Conditions/weather/phenomena-Ceiling/visibility/precip-Low visibility-Effect on operation | `C` | `0303501582` |
| 1 | 7 | `F` | `T` | Environmental issues-Conditions/weather/phenomena-Light condition-Dark-Decision related to condition | `F` | `0303602084` |
| 1 | 8 | `-` | `F` | Environmental issues-Conditions/weather/phenomena-Ceiling/visibility/precip-Low visibility-Contributed to outcome | `-` | `0303501591` |
| 1 | 9 | `-` | `F` | Environmental issues-Conditions/weather/phenomena-Ceiling/visibility/precip-Low visibility-Awareness of condition | `-` | `0303501587` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 2193 words

> HISTORY OF FLIGHTOn April 15, 2018, at 2054 eastern daylight time, a Cessna 525, N525P, was destroyed after it impacted terrain near Crozet, Virginia. The private pilot was fatally injured. The airplane was owned by a private individual and was being operated under the provisions of Title 14 Code of Federal Regulations (CFR) Part 91 as a personal flight. Night instrument meteorological conditions prevailed at the time of the accident, and no flight plan was filed for the flight, which departed Richmond Executive–Chesterfield County Airport (FCI), Richmond, Virginia, about 2035 and was destined for Shenandoah Valley Regional Airport (SHD), Weyers Cave, Virginia.
> 
> According to a friend of the pilot, the pilot had "a couple of drinks" while they were preparing dinner. The pilot left her home about 1930. The pilot's friend thought that the pilot would be going to a hotel because it was getting dark, but FCI security video showed that the pilot arrived at the airport at 2002 and walked to the airplane at 2004. The pilot then walked around the airplane for about 3 minutes, boarded the airplane, closed the main cabin door, and initiated the engine start sequence at 2017. About 2 minutes later, the airplane began to taxi to the departure end of runway 15 and then taxied back to the departure end of runway 33. The takeoff roll began on runway 33 at 2033. The airport security video showed the windsock, which indicated that the wind favored a departure from runway 15. According to an airport line service employee, the airplane departed with a tailwind. The employee also stated that the pilot did not communicate on the Unicom frequency.
> 
> According to air traffic control data provided by the Federal Aviation Administration (FAA), a radar target identified as the accident airplane departed FCI and reached a maximum altitude of about 11,500 ft mean sea level (msl) at 2040. The airplane then began to descend and, at 2044, leveled off at an altitude of about 4,300 ft (which was below the minimum safe altitude of 5,700 ft msl for SHD). The airplane remained at 4,300 ft until 2053, when it began a descending left turn. The last two radar returns were 5 seconds apart and showed the airplane at 3,300 ft and 2,800 msl, which indicated that the airplane was descending about 6,000 ft per minute. Radar contact was lost at 2054. Throughout the flight, the pilot did not have any contact with air traffic control.
> 
> According to a witness near the accident location, he heard the "screaming of the engines" and then felt the terrain shake when the airplane impacted the ground. He stated that, at the time of the accident, the cloud ceiling was "really low," the winds were moderate, and heavy rain was occurring. PERSONNEL INFORMATIONAccording to FAA airman records, the pilot held a private pilot certificate with ratings for airplane single-engine land, multiengine land, and instrument airplane. In addition, the pilot had a Cessna CE-525S type rating. The pilot was issued a third-class medical certificate on November 30, 2016. At that time, he reported 1,900 hours of total flight experience, of which 25 hours were within the previous 6 months.
> 
> According to the pilot's logbook, he had a total of 737.9 hours of flight time, of which 13.5 hours were in the 30 days before the accident. In addition, he reported 1.4 hours of instrument time in the previous 90 days, which included 9 instrument approaches. Since 2014, the pilot had flown 165.4 hours in the accident airplane. According to family members, the pilot flew to Richmond, Virginia, the day before the accident to perform a flight review on the afternoon of the accident date. AIRCRAFT INFORMATIONAccording to FAA airworthiness records, the airplane was manufactured in 1996 and was equipped with two Williams International FJ44-1A engines, each of which produced 1,900 lbs of thrust. According to the maintenance logbooks, the most recent continuous airworthiness inspection was recorded on March 1, 2017; at that time, the airframe had accumulated 3,311.6 total hours of operation.
> 
> According to FAA airworthiness records, the airplane was equipped with a multifunction display and a Garmin MX20, which displayed satellite weather information. According to the Garmin MX20 description, the display had a built-in terrain elevation database that color-coded relevant ground features in relation to an aircraft's altitude and could alert the pilot to rising terrain. The MX20 was also integrated with various onboard weather radar, lightning, traffic awareness, and datalink systems that enabled uploading of graphical weather information and Next Generation Weather Radar depictions. METEOROLOGICAL INFORMATIONThe recorded weather conditions at FCI about the time of departure indicated wind from 140° at 12 knots, 10 miles visibility, and broken cloud ceilings at 3,200 and 4,000 ft above ground level (agl).
> 
> The 2057 recorded weather observation at Charlottesville-Albemarle Airport (CHO), Charlottesville, Virginia, which was about 13 miles northeast of the accident location, included wind from 020° at 4 knots, visibility 2 ½ miles, rain and mist, broken clouds at 700 ft agl, overcast clouds at 1,500 ft agl, temperature 11°C, dew point 11°C, and an altimeter setting of 29.79 inches of mercury. The remarks section indicated that lightning was detected northeast and south of the airport.
> 
> The 2035 recorded weather observation at SHD, which was about 15 miles northwest of the accident site, indicated wind from 350° at 12 knots, 7 miles visibility, moderate rain, scattered clouds at 900 ft agl, broken ceiling at 4,700 ft agl, overcast clouds at 5,000 ft agl, temperature 11°C, dew point 11°C, and an altimeter setting of 29.77 inches of mercury. The remarks section stated that the station had a precipitation discriminator and provided the following information: lightning distant (beyond 10 miles but less than 30 miles from the center of the airport) southeast, 0.29 inch of precipitation since 1955, temperature 11.1°C, and dew point 10.5°C.
> 
> The 2035 recorded automated weather observation at Eagles Nest Airport (W13), Waynesboro, Virginia, which was about 12 miles southwest of the accident location, indicated wind from 040° at 3 knots, 7 miles visibility, scattered clouds at 600 ft agl, broken ceiling at 1,600 ft agl, overcast clouds at 4,400 ft agl, temperature 14°C, dew point 14°C, and an altimeter setting of 29.74 inches of mercury. The remarks indicated that the station did not have a precipitation discriminator and provided the following information: 0.14 inch of precipitation since 1955, temperature 13.7°C, and dew point 13.6°C.
> 
> According to Lockheed Martin Flight Services, for the accident flight, the pilot did not obtain a weather briefing or use the direct user access terminal service.
> 
> According to reviewed radar data, reflectivity values between 25 and 35 dBZ were located above the accident site at 2053 (see figure 1), which corresponded with the surface observation precipitation reports from W13, SHD, and CHO. The reflectivity bands were moving from south-southwest to north-northeast between 2004 and 2103. The reflectivity targets indicated of moderate-to-heavy rain moving northward across the accident site at the accident time.
> 
> The accident airplane flew through a thunderstorm line between 2042 and 2047. There were no lightning strikes within 10 miles of the accident site about the accident time.
> 
> 
> 
> 
> 
> Figure 1. Radar reflectivity at 2053 with the accident site marked with a black circle, the accident flight track in pink, the airplane's position at 2053 marked with a red circle and the lightning flashes represented by the black dots.
> 
> 
> 
> Further, two convective SIGMET advisories were valid for the accident site at the accident time. SIGMET 31E, issued at 1855 and valid through 2055, warned of a line of severe thunderstorms moving from 210° at 40 knots with cloud tops to FL420 (about 42,000 ft) with tornadoes, hail with a size up to 1 inch, and wind gusts to 60 knots possible. SIGMET 36E, issued at 1955 and valid through 2155, contained the same severe thunderstorm information as SIGMET 31E except that the cloud tops were to FL410 (about 41,000 ft).
> 
> AIRMETs Sierra, Tango, and Zulu were valid for the accident site at the accident time. The AIRMETs warned of instrument flight rules conditions due to precipitation and mist; mountain obscuration conditions due to clouds, precipitation, and mist; moderate turbulence below FL180 (about 18,000 ft), low-level wind shear conditions, and moderate icing below FL240 (about 24,000 ft).
> 
> In addition, there were three urgent pilot reports for the area near CHO within the 2 hours that preceded the time of the accident. All three reports were from Bombardier CRJ-200 airplanes. The reports stated that there was moderate turbulence in the vicinity, and one of the reports stated that the cloud bases were overcast at 1,500 ft msl.
> 
> According to the Astronomical Applications Department at the US Naval Observatory, for the area of the accident, sunset was at 1951, and the end of civil twilight was at 2018. Moonrise was at 0644, and the phase of the moon was a new moon at 2157. AIRPORT INFORMATIONAccording to FAA airworthiness records, the airplane was manufactured in 1996 and was equipped with two Williams International FJ44-1A engines, each of which produced 1,900 lbs of thrust. According to the maintenance logbooks, the most recent continuous airworthiness inspection was recorded on March 1, 2017; at that time, the airframe had accumulated 3,311.6 total hours of operation.
> 
> According to FAA airworthiness records, the airplane was equipped with a multifunction display and a Garmin MX20, which displayed satellite weather information. According to the Garmin MX20 description, the display had a built-in terrain elevation database that color-coded relevant ground features in relation to an aircraft's altitude and could alert the pilot to rising terrain. The MX20 was also integrated with various onboard weather radar, lightning, traffic awareness, and datalink systems that enabled uploading of graphical weather information and Next Generation Weather Radar depictions. WRECKAGE AND IMPACT INFORMATIONThe airplane impacted three 40-ft trees about 15 ft before impacting terrain at an elevation of 1,520 ft msl. The impact location was about 450 ft from the last radar return. The initial impact crater was about 4 ft deep, and a scent similar to Jet A fuel was noted at the accident site. The airplane was highly fragmented, with all major components of the airplane located at the accident site. The debris path emanated from a 120° heading, and the accident site was on a 25° incline.
> 
> All flight control cables and bellcranks remained attached in their appropriate locations and showed evidence of overstress failures.
> 
> The standby attitude indicator was located along the debris field and was disassembled. The gyro housing exhibited rotational scoring.
> 
> The left engine had separated due to impact forces and was located in the initial impact crater. The compressor turbine blades were damaged by the impact, and rotational scoring was noted on the blades. The turbine blade bases exhibited rotational scoring.
> 
> The right engine had separated due to impact forces and was located about 60 ft beyond the initial impact location. The engine was partially consumed by fire. The compressor fan blades exhibited rotational scoring, and several blades were bent forward. In addition, the compressor turbine blade housing exhibited rotational scoring, and the blades were bent the opposite direction of travel. ADDITIONAL INFORMATIONFAA Airplane Flying Handbook
> 
> The handbook provided the following information about an airplane's attitude and spatial disorientation:
> 
> The pilot must believe what the flight instruments show about the airplane's attitude regardless of what the natural senses tell. The vestibular sense (motion sensing by the inner ear) can and will confuse the pilot. Because of inertia, the sensory areas of the inner ear cannot detect slight changes in airplane attitude, nor can they accurately sense the attitude changes that occur at a uniform rate over a period of time. On the other hand, false sensations are often generated, leading the pilot to believe the attitude of the airplane has changed when, in fact, it has not. These false sensations result in the pilot experiencing spatial disorientation. MEDICAL AND PATHOLOGICAL INFORMATIONThe Commonwealth of Virginia Department of Health, Office of the Chief Medical Examiner, Richmond, Virginia, performed the autopsy of the pilot. The autopsy report indicated that the pilot died as a result of multiple blunt force injuries.
> 
> Toxicology testing performed at the FAA's Forensic Sciences Laboratory identified ethanol (0.
> 080 gm/hg, which equates to 0.080 gm/dl) and cetirizine in the pilot's muscle tissue.
> Ethanol is the intoxicant commonly found in beer, wine, and liquor. It acts as a central nervous system depressant and impairs judgment, psychomotor functioning, and vigilance. The effects of ethanol on aviators are generally well understood: it significantly impairs a pilot's performance, even at very low levels. Title 14 CFR 91.17(a) prohibits any person from acting or attempting to act as a crewmember of a civil aircraft while having 0.040 gm/dl or more ethanol in the blood. In addition, the regulation states that no person can act as a crewmember of an aircraft within 8 hours after the consumption of any alcoholic beverage. Ethanol can also be produced in body tissues postmortem.
> 
> Cetirizine is a sedating antihistamine available over the counter and by prescription. It carries this warning for patients: "when using this product…drowsiness may occur…avoid alcoholic drinks…alcohol, sedatives, and tranquilizers may increase drowsiness…be careful when driving a motor vehicle or operating machinery."

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's loss of control while operating in night instrument meteorological conditions as a result of spatial disorientation. Contributing to the accident was the pilot's decision to operate an airplane after consuming alcohol and his resulting intoxication, which degraded the pilot's judgment and decision-making.

- duplicate stripped finding descriptions in this event: **0**

---

## 12. `20190430X15852` — GAA19CA231

- date: `04/26/19 00:00:00`  year `2019`  type `ACC`
- location: St Charles, MO USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Aircraft-Aircraft systems-Landing gear system-Gear extension and retract sys-Not used/operated | `C` | `0102323010` |
| 1 | 2 | `C` | `T` | Personnel issues-Action/decision-Action-Lack of action-Student/instructed pilot | `C` | `0204103046` |
| 1 | 3 | `F` | `T` | Personnel issues-Task performance-Use of equip/info-Use of checklist-Student/instructed pilot | `F` | `0206303046` |
| 1 | 4 | `F` | `T` | Personnel issues-Psychological-Attention/monitoring-Monitoring other person-Instructor/check pilot | `F` | `0202153540` |
| 1 | 5 | `-` | `F` | Environmental issues-Conditions/weather/phenomena-Wind-(general)-Contributed to outcome | `-` | `0303400091` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 114 words

> The flight instructor reported that during the instructional flight accomplishing takeoffs and landings, during the seventh landing, the landing checklist was called, but due to the "wind effects", the landing gear was not extended. During the approach, the airplane was configured with the left engine operating normally while the right engine was operating to simulate zero thrust. The airplane touched down on the runway centerline with the landing gear retracted.  The airplane slid to the left, exited the runway, and impacted a landing light fixture.  The lower fuselage longerons were substantially damaged. 
> 
> The flight instructor reported that there were no preaccident mechanical failures or malfunctions with the airplane that would have precluded normal operation.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot receiving instruction's failure to extend the landing gear. Contributing to the accident were the pilot receiving instruction's failure to complete the landing checklist and the flight instructor's inadequate monitoring of the pilot.

- duplicate stripped finding descriptions in this event: **0**

---

## 13. `20160204X80119` — WPR16LA063

- date: `02/03/16 00:00:00`  year `2016`  type `ACC`
- location: San Diego, CA USA
- Aircraft_Key values in findings: `[1, 2]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Psychological-Attention/monitoring-Task monitoring/vigilance-Instructor/check pilot | `C` | `0202152040` |
| 1 | 2 | `F` | `T` | Personnel issues-Action/decision-Action-Delayed action-Instructor/check pilot | `F` | `0204102540` |
| 2 | 1 | `C` | `T` | Personnel issues-Psychological-Attention/monitoring-Task monitoring/vigilance-Pilot of other aircraft | `C` | `0202152045` |
| 2 | 2 | `F` | `T` | Personnel issues-Action/decision-Action-Delayed action-Pilot of other aircraft | `F` | `0204102545` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 406 words

> On February 3, 2016, about 1130 Pacific standard time, a Cessna 172S, N499DR, impacted a parked, occupied Cessna 172S, N1955L at the Gillespie Field Airport (SEE), San Diego/El Cajon, California. Both airplanes were occupied with one certified flight instructor (CFI) and one student pilot; no one was injured. N499DR sustained minor damage, and N1955L sustained substantial damage to the fuselage structure and rudder. Both airplanes were registered to Sorbi Aviation Inc., and were operated by the California Flight Academy as 14 Code of Federal Regulations Part 91 instructional flights. Visual meteorological conditions prevailed at the time of the accident and neither airplane had filed a flight plan. Both airplanes were on the California Flight Academy parking ramp preparing for their local flights. 
> 
> The CFI from N499DR reported that this was the student pilot's first flight lesson. After completing a thorough preflight they hand towed the airplane out from its north facing parking spot and turned it towards the east. They started the engine and it idled between 800-1000 RPM. While listening to the airport's automatic terminal information service (ATIS) the airplane started to move with a right turning tendency. The CFI stated he did not notice it at first, but when he did, he stepped on the brakes. The airplane increased its right turn and struck a parked, occupied, airplane (N1955L). In a later conversation, the CFI reported that when he attempted to stop the airplane he noticed that the right rudder pedal was slightly more forward than the left, but not by much. 
> 
> In a written statement, the student pilot from N499DR reported that when the CFI was listening to the radio, the airplane started moving and turning into another airplane. He stated "Hey you! Airplane is moving!" and he touched the CFI. The CFI looked at him, then back at the radio, and he "did not do anything;" he appeared to be distracted. The airplane continued its turn and impacted N1955L.
> 
> The CFI of N1955L reported that the student pilot and he were preparing for their flight with the engine off, when they suddenly felt a jolt and heard the sound of metal contacting metal. They turned around and observed that N499DR had struck the aft fuselage of their airplane.  
> 
> During a postaccident examination of N499DR's brake system by a Federal Aviation Administration airworthiness inspector, there were no visual defects or leaks. He manipulated the brakes both dependently and independently with no anomalies noted.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The flight instructor’s failure to maintain awareness while parked on the ramp with the engine operating, which resulted in impact with another parked airplane.


### Aircraft_Key 2 — `narr_accp` FACTUAL NARRATIVE (model-visible), 406 words

> On February 3, 2016, about 1130 Pacific standard time, a Cessna 172S, N499DR, impacted a parked, occupied Cessna 172S, N1955L at the Gillespie Field Airport (SEE), San Diego/El Cajon, California. Both airplanes were occupied with one certified flight instructor (CFI) and one student pilot; no one was injured. N499DR sustained minor damage, and N1955L sustained substantial damage to the fuselage structure and rudder. Both airplanes were registered to Sorbi Aviation Inc., and were operated by the California Flight Academy as 14 Code of Federal Regulations Part 91 instructional flights. Visual meteorological conditions prevailed at the time of the accident and neither airplane had filed a flight plan. Both airplanes were on the California Flight Academy parking ramp preparing for their local flights. 
> 
> The CFI from N499DR reported that this was the student pilot's first flight lesson. After completing a thorough preflight they hand towed the airplane out from its north facing parking spot and turned it towards the east. They started the engine and it idled between 800-1000 RPM. While listening to the airport's automatic terminal information service (ATIS) the airplane started to move with a right turning tendency. The CFI stated he did not notice it at first, but when he did, he stepped on the brakes. The airplane increased its right turn and struck a parked, occupied, airplane (N1955L). In a later conversation, the CFI reported that when he attempted to stop the airplane he noticed that the right rudder pedal was slightly more forward than the left, but not by much. 
> 
> In a written statement, the student pilot from N499DR reported that when the CFI was listening to the radio, the airplane started moving and turning into another airplane. He stated "Hey you! Airplane is moving!" and he touched the CFI. The CFI looked at him, then back at the radio, and he "did not do anything;" he appeared to be distracted. The airplane continued its turn and impacted N1955L.
> 
> The CFI of N1955L reported that the student pilot and he were preparing for their flight with the engine off, when they suddenly felt a jolt and heard the sound of metal contacting metal. They turned around and observed that N499DR had struck the aft fuselage of their airplane.  
> 
> During a postaccident examination of N499DR's brake system by a Federal Aviation Administration airworthiness inspector, there were no visual defects or leaks. He manipulated the brakes both dependently and independently with no anomalies noted.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The failure of the flight instructor of the other airplane to maintain awareness while parked on the ramp with the engine operating, which resulted in impact with the parked airplane.

- duplicate stripped finding descriptions in this event: **0**

---

## 14. `20140430X90625` — WPR14CA178

- date: `04/29/14 00:00:00`  year `2014`  type `ACC`
- location: Rexburg, ID USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 2 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Directional control-Not attained/maintained | `C` | `0106202020` |
| 1 | 3 | `F` | `T` | Personnel issues-Task performance-Communication (personnel)-CRM/MRM techniques-Flight crew | `F` | `0206354036` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 197 words

> The pilot stated that he was in the left seat and a pilot rated passenger, who was a certified flight instructor (CFI), was in the right seat. The flight instructor stated that his seat was positioned aft such that he could not reach the rudder pedals. The pilot positioned the airplane on runway 35 for takeoff and said that he rotated a little bit early (70 knots) during the takeoff roll but it was manageable. The flight instructor stated that the airplane swerved left and right before the pilot rotated. The flight instructor called out to bring the throttle back, and described the remaining portion of the flight as porpoising. Both pilots reported that there was confusion in the cockpit. 
> 
> A witness said that he observed the airplane rotate early, enter a steep nose high attitude, and then begin to settle while the elevator was moving up and down erratically. After skidding for 497 feet the airplane went off the end of the runway and into brush causing substantial damage to some fuselage bulkheads and the right wing spar.
> 
> The pilot reported no preimpact mechanical malfunctions or failures with the airplane that would have precluded normal operation.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's loss of directional control and early rotation during takeoff. Contributing to the accident was the failure of the pilots to exercise adequate communication techniques.

- duplicate stripped finding descriptions in this event: **0**

---

## 15. `20170527X93038` — WPR17FA108

- date: `05/27/17 00:00:00`  year `2017`  type `ACC`
- location: Haines, AK USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Action/decision-Info processing/decision-Decision making/judgment-Pilot | `C` | `0204152044` |
| 1 | 2 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 3 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Airspeed-Not attained/maintained | `C` | `0106201020` |
| 1 | 4 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Lateral/bank control-Incorrect use/operation | `C` | `0106202311` |
| 1 | 5 | `F` | `T` | Aircraft-Aircraft systems-Electrical power system-Alternator-generator drive sys-Inoperative | `F` | `0102241026` |
| 1 | 6 | `F` | `T` | Aircraft-Aircraft systems-Electrical power system-Alternator-generator drive sys-Fatigue/wear/corrosion | `F` | `0102241006` |
| 1 | 7 | `F` | `T` | Aircraft-Aircraft systems-Electrical power system-Battery/charger-Damaged/degraded | `F` | `0102243205` |
| 1 | 8 | `F` | `T` | Personnel issues-Action/decision-Info processing/decision-Decision making/judgment-Pilot | `F` | `0204152044` |
| 1 | 9 | `-` | `F` | Personnel issues-Task performance-Maintenance-Scheduled/routine maintenance-Pilot | `-` | `0206201044` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 2954 words

> HISTORY OF FLIGHTOn May 27, 2017, about 1101 Alaska daylight time, a Piper PA-30, airplane, N7376Y, collided with the ground shortly after a low-level pass over a remote airstrip at Glacier Point, which is located 12 miles southeast of Haines, Alaska. The pilot and a pilot-rated passenger in the right front seat were fatally injured, and a rear-seated passenger was seriously injured. The airplane was registered to the pilot who was operating it under the provisions of Title 14 Code of Federal Regulations Part 91 as a personal flight. Visual meteorological conditions prevailed at the time of the accident, and a flight plan was not filed. The flight originated from Juneau International Airport (PAJN), Juneau, Alaska, about 1015 and was destined for Haines Airport (PAHN), Haines, Alaska.
> 
> An eyewitness located across Chilkat Inlet, which was about 2 miles east of the shoreline of Glacier Point, and using binoculars saw the accident airplane flying northbound at tree level near the airstrip. He stated that, as the airplane reached the end of the airstrip, it dropped in altitude, banked to the right, and impacted the shoreline in a right-wing-down, nose-down attitude. The airplane came to rest near the edge of a canal about 1/4-mile northeast of the north end of the airstrip (See Figure 1). The eyewitness and three other people responded to the accident site by boat and called local authorities when cell coverage was available when they were about halfway across the canal. According to the eyewitness, as they arrived at the accident site, the rear-seated passenger was the only airplane occupant who was responsive, but he could not be removed from the airplane. Within minutes, tidal water was surrounding and flooding the airplane. A tractor brought to the site from a local tour facility was used to drag the airplane to shallow water. Local authorities arrived soon after and extricated the passengers.
> 
> 
> 
> 
> 
> Figure 1-Aerial Image of the Accident Site
> 
> According to the rear-seated passenger aboard the accident airplane, about 20 minutes into the flight, the pilot intentionally shut down the right engine to demonstrate how to restart the engine during flight. Despite several attempts, the engine would not restart with electrical power. The pilot then made several attempts to air start the engine by gaining altitude and then diving the airplane down to use airflow to assist in rotating the engine. After two unsuccessful attempts to air start the engine, the pilot decided to descend to a lower altitude, fly to the airstrip at Glacier Point, and use the battery booster (which was located in the baggage compartment) after landing to start the engine. As the airplane approached the airstrip, the pilot made a low-level pass to check the condition of the airstrip surface; this was the last thing the passenger remembered about the flight.
> 
> A friend of the pilot reported that he flew with the accident pilot in the accident airplane on the day before the accident. The friend stated that he and the pilot were preparing to depart PAJN for a planned flight to Gustavus Airport (PAGS), Gustavus, Alaska. As the airplane was taxiing to depart, the left engine "stalled" on the taxiway, and the pilot could not restart the engine using the starter due to low electrical power from the battery. They taxied back to the pilot's hangar, where they removed a battery from his hangered floatplane and installed it in the accident airplane. Despite these actions, both engines could not be started. The friend said that the floatplane battery did not supply enough electrical power to start the airplane engine. The pilot then parked his motor vehicle near the airplane, plugged in the airplane's jumper cables, and successfully jumpstarted both engines from the vehicle's battery. The pilot and his friend departed PAJN on an uneventful flight to PAGS. The friend stated that the pilot told him that he normally had a handheld battery booster in the airplane but that he had loaned it to the ground personnel at PAJN because they had a hard time starting the airport's fuel truck. PERSONNEL INFORMATIONThe pilot, age 29, held a private pilot certificate with multiengine land and single-engine land and sea ratings. The pilot's most recent FAA third-class airman medical certificate was issued on January 30, 2013, with no limitations. On his medical application, the pilot reported that his total flight experience during the previous 6 months was 0 hours. The pilot's logbook was not located during the investigation. AIRCRAFT INFORMATIONThe airplane, which was manufactured in 1964, was an all-metal multiengine airplane that incorporated a semi-monocoque fuselage and empennage design. The airplane was equipped with fully cantilevered wings, electrically operated wing flaps, and electrically operated retractable tricycle landing gear.
> 
> The airplane was powered by a Lycoming IO-320-B1A reciprocating engine on the left wing and a Lycoming LIO-320-B1A reciprocating engine on the right wing, and each was rated at 160 horsepower. The engines had 4 cylinders, 320-cubic-inch displacement, and fuel injection. The right engine had a counter-rotating kit installed. Each engine drove a Hartzell 2-blade, single-acting, hydraulically operated, constant-speed propeller with feathering capability.
> 
> The airplane's electrical power was supplied by a 12-volt, direct-current, negative-ground system. The primary electrical source came from two 12-volt, 50-ampere alternators controlled by an overvoltage relay and voltage regulator. The overvoltage relay and voltage regulator were mounted on the aft bulkhead of the nose section. Secondary power was provided by a 12-volt, 35-ampere hour battery that supplies power for starting and was a reserve power source in the event of an alternator failure. The battery was mounted in a battery box located immediately aft of the baggage compartment. The amp/voltmeter instrument was installed in the instrument panel. Alternator isolation switches were mounted on the instrument panel.
> 
> According to FAA records, the airplane's charging system was modified on December 8, 1993, by the removal of the generators and installation of an alternator charging system in accordance with Supplement Type Certificate (STC) SA334SW. If both alternators were inoperative, the airplane battery would be the only remaining source of electrical power. If the airplane battery were depleted and electrical power was not available, the Piper Twin Comanche PA-30 Pilot's Operating Handbook (POH) stated that the pilot must land with the flaps in the retracted position and must initiate the manual gear extension procedure and that the final approach landing speed must not exceed 100 mph or 87 knots.
> 
> The airplane was also modified with LoPresti front engine cowlings in accordance with STC SA3302SO. The cowling modification would not have permitted a visual examination of the front side of the engine and the alternator belts during a preflight walk-around inspection unless the upper cowling was removed.
> 
> The last entry in the airframe maintenance records was on August 20, 2014, when the last annual inspection was accomplished. At that time, the airplane had accumulated a total of 4,769 flight hours. No engine maintenance records were found. The airplane's Hobbs meter was not found in the wreckage. Due to impact damage to the cabin's digital instruments, the tachometer time at the time of the accident could not be determined. METEOROLOGICAL INFORMATIONAt 1054, PAHN, located about 12 miles north of the accident site, reported the following conditions: wind from 150° at 7 knots, 10 miles visibility, clear skies, temperature 11°C, dew point 6°C, and an altimeter setting of 30.23 inches of mercury. AIRPORT INFORMATIONThe airplane, which was manufactured in 1964, was an all-metal multiengine airplane that incorporated a semi-monocoque fuselage and empennage design. The airplane was equipped with fully cantilevered wings, electrically operated wing flaps, and electrically operated retractable tricycle landing gear.
> 
> The airplane was powered by a Lycoming IO-320-B1A reciprocating engine on the left wing and a Lycoming LIO-320-B1A reciprocating engine on the right wing, and each was rated at 160 horsepower. The engines had 4 cylinders, 320-cubic-inch displacement, and fuel injection. The right engine had a counter-rotating kit installed. Each engine drove a Hartzell 2-blade, single-acting, hydraulically operated, constant-speed propeller with feathering capability.
> 
> The airplane's electrical power was supplied by a 12-volt, direct-current, negative-ground system. The primary electrical source came from two 12-volt, 50-ampere alternators controlled by an overvoltage relay and voltage regulator. The overvoltage relay and voltage regulator were mounted on the aft bulkhead of the nose section. Secondary power was provided by a 12-volt, 35-ampere hour battery that supplies power for starting and was a reserve power source in the event of an alternator failure. The battery was mounted in a battery box located immediately aft of the baggage compartment. The amp/voltmeter instrument was installed in the instrument panel. Alternator isolation switches were mounted on the instrument panel.
> 
> According to FAA records, the airplane's charging system was modified on December 8, 1993, by the removal of the generators and installation of an alternator charging system in accordance with Supplement Type Certificate (STC) SA334SW. If both alternators were inoperative, the airplane battery would be the only remaining source of electrical power. If the airplane battery were depleted and electrical power was not available, the Piper Twin Comanche PA-30 Pilot's Operating Handbook (POH) stated that the pilot must land with the flaps in the retracted position and must initiate the manual gear extension procedure and that the final approach landing speed must not exceed 100 mph or 87 knots.
> 
> The airplane was also modified with LoPresti front engine cowlings in accordance with STC SA3302SO. The cowling modification would not have permitted a visual examination of the front side of the engine and the alternator belts during a preflight walk-around inspection unless the upper cowling was removed.
> 
> The last entry in the airframe maintenance records was on August 20, 2014, when the last annual inspection was accomplished. At that time, the airplane had accumulated a total of 4,769 flight hours. No engine maintenance records were found. The airplane's Hobbs meter was not found in the wreckage. Due to impact damage to the cabin's digital instruments, the tachometer time at the time of the accident could not be determined. WRECKAGE AND IMPACT INFORMATIONThe impact site was located on the western tidal flats of the Chilkat Inlet, about 1/4-mile northeast of the north end of the airstrip at Glacier Point.
> 
> The initial on-scene examination of the airplane by the NTSB-IIC and a Federal Aviation Administration inspector revealed impact damage consistent with a right-wing-down, nose-down attitude during ground impact. The airplane remained intact, all flight control surfaces were accounted for, and cable control continuity was confirmed. The landing gear was in the down position, and the landing gear position switch was in the down position. The landing gear extension motor release arm was found in the disengaged position. The emergency landing gear extension handle was removed from its stowed position and installed in a socket on the emergency disengage control. The flaps were in the up position and the flap lever was in the down position.
> 
> Both engines separated from their wing mounts and remained partially attached to their wings by control cables and tubing. One of the left propeller blades was in a feathered/high pitch position and the other blade was rotated toward a high pitch position that was beyond the feathered position. Both blades exhibited leading edge gouging, twisting toward high pitch and bending in the forward/thrust direction. Heavy chordwise/rotational scoring damage was isolated to the face side of both blades. One blade tip had fractured and separated; the separated tip was recovered at the crash site. The right propeller was found with both blades in the feathered position. One blade was bent rearward with no remarkable twisting, and one blade had no remarkable damage. The elevator trim actuator was found in the full nose-down position and the rudder trim indicator was in the nose-left position.
> 
> The wreckage was relocated to a hangar at PAGS, and examination of the wreckage showed that the right engine crankshaft propeller flange was bent to one side and that the rocker covers had impact damage. The right engine's exterior surfaces had a dark oily residue. Oil residue was observed in the area of the alternator pulley and belt. The right engine alternator was undamaged and secure, and no signatures suggested that the alternator was repositioned during the accident sequence. The alternator electrical wiring remained secure at the terminals. The alternator drive pulley rotated freely by hand, and the drive belt remained stationary with the crankshaft. The right engine alternator drive belt was loose when examined and was subsequently removed from the engine. The belt was excessively worn on the pulley contact area as shown in Figure 2.  A spare alternator drive belt was found stowed to the engine; the stowed belt shared the same part numbers as the worn belt (Napa Premium XL 25-7365). According to the alternator STC installation instructions, a Franklin (P/N 14883) or a Goodyear 5L380 belts should be used.
> 
> 
> 
> 
> 
> Figure 2-Right Engine Alternator Belt
> 
> 
> 
> 
> The right engine inlet cowling section had rubber filings in the forward right interior surface. Rubber filings were also found on the back side of the starter ring gear and surrounding areas.The left engine alternator was undamaged and secure, and no signatures suggested that the alternator was repositioned during the accident sequence. The alternator electrical wiring remained secure at each terminal. No belt was attached to the alternator pully, and no belt was recovered within the confines of the engine cowling. The alternator drive pulley forward face had impact damage, bending the edge of the forward face aft into the location where the drive belt would be positioned. There was no corresponding damage to the engine cowling in the area of the alternator pulley that would have resulted in damage to the alternator pulley. The alternator drive shaft rotated freely by hand. The alternator housing was covered in surface corrosion consistent to being submerged in salt water. A dark residue covered the forward side of the alternator and the drive pulley. The belt contact area in the alternator drive belt pulley and the crankshaft pulley was also covered in a dark residue.
> 
> The airplane battery separated from the main wreckage and remained in the battery box. The battery housing had impact damage revealing internal components. The terminal connections remained attached to the battery. A date of "6/15" was written on the top of the battery.
> 
> The amp/voltmeter instrument was removed from the instrument panel. The amp/volt selection toggle switch was damaged and found in the amp position.
> 
> The alternator isolation switches were found in the "ON" position. There were no annunciator lights or warning system that would have indicated either alternator had stopped working during operations.
> 
> A multimeter and battery jump-starter unit was found within the wreckage. ADDITIONAL INFORMATIONThe FAA's Airplane Flying Handbook states the following:
> 
> The basic difference between operating a multiengine airplane and a single-engine airplane is the potential problem involving an engine failure. The penalties for loss of an engine are twofold: performance and control. The most obvious problem is the loss of 50 percent of power, which reduces climb performance 80 to 90 percent, sometimes even more. The other is the control problem caused by the remaining thrust, which is now asymmetrical. Attention to both these factors is crucial to safe one engine inoperative (OEI) flight. The performance and systems redundancy of a multiengine airplane is a safety advantage only to a trained and proficient pilot.
> 
> Although it is a natural desire among pilots to save an ailing engine with a precautionary shutdown, the engine should be left running if there is any doubt as to needing it for further safe flight. Catastrophic failure accompanied by heavy vibration, smoke, blistering paint, or large trails of oil, on the other hand, indicate a critical situation. The affected engine should be feathered and the Securing Failed Engine checklist completed. The pilot should divert to the nearest suitable airport and declare an emergency with ATC for priority handling.
> 
> There are two different sets of bank angles used in OEI flight.
> 
> 1. To maintain directional control of a multiengine airplane suffering an engine failure at low speeds (such as climb), momentarily bank at least 5° and a maximum of 10° towards the operative engine as the pitch attitude for VYSE [best rate of climb speed with OEI] is set. This maneuver should be instinctive to the proficient multiengine pilot and take only 1 to 2 seconds to attain. It is held just long enough to assure directional control as the pitch attitude for VYSE is assumed.
> 
> 2. To obtain the best climb performance, the airplane must be flown at VYSE and zero sideslip with the failed engine feathered and maximum available power from the operating engine. Zero sideslip is approximately 2° of bank toward the operating engine and a one-third to one-half ball deflection also toward the operating engine. The precise bank angle and ball position varies somewhat with make and model and power available. If above the airplane's single-engine ceiling, this attitude and configuration results in the minimum rate of sink.
> 
> In OEI flight at low altitudes and airspeeds such as the initial climb after takeoff, pilots must operate the airplane so as to guard against the three major accident factors: (1) loss of directional control, (2) loss of performance, and (3) loss of flying speed. All have equal potential to be lethal. Loss of flying speed is not a factor, however, when the airplane is operated with due regard for directional control and performance. MEDICAL AND PATHOLOGICAL INFORMATIONThe State Medical Examiner's Office in Anchorage, Alaska, conducted autopsies on the pilot and pilot-rated passenger.  The pilot's cause of death was reported as "Blunt impacts ..." The pilot-rated passengers cause of death was also reported as blunt impacts.
> 
> Toxicology testing performed at the FAA Forensic Sciences Laboratory were negative on both the pilot and pilot-rated passenger for drugs, carbon monoxide and volatiles.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's decision to turn toward the inoperative engine after conducting a low-level pass, which resulted in an aerodynamic stall at too low an altitude to recover. Contributing to the accident was the pilot's decision to perform the flight and the engine shut down demonstration with an inadequate airplane charging system and a known weak battery.

- duplicate stripped finding descriptions in this event: **1**

---

## 16. `20120130X60836` — ERA12LA165

- date: `01/28/12 00:00:00`  year `2012`  type `ACC`
- location: Palm Beach, FL USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `F` | `T` | Aircraft-Fluids/misc hardware-Fluids-Fuel-Fluid level | `F` | `0107101024` |
| 1 | 2 | `C` | `T` | Personnel issues-Action/decision-Info processing/decision-Decision making/judgment-Pilot | `C` | `0204152044` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 1909 words

> HISTORY OF FLIGHTOn January 28, 2012, about 1430 eastern standard time, a Piper PA-31-310, N30DC, was substantially damaged during a forced landing to a beach in Palm Beach, Florida, following a loss of engine power in both engines. The airline transport pilot was not injured. The airplane was registered to and operated by Secure Aviation, Inc., under 14 Code of Federal Regulations Part 91. Visual meteorological conditions prevailed, and a visual flight rules fight plan was filed for the personal flight, which originated at San Salvador International Airport (MYSM), San Salvador, The Bahamas, around 1220. The intended destination was St. Lucie County International Airport (FPR), Fort Pierce, Florida.
> 
> According to the pilot, the accident occurred on the inbound leg to the United States, with the airplane having flown an outbound leg the same day. Flight planning was completed on the day before the flights, with 2.0 hours planned outbound and 2.5 hours inbound. Planned fuel consumption was for 150 to 160 gallons used with 26 to 36 useable remaining.
> 
> On the morning of the accident, the pilot flew the airplane first to Palm Beach International Airport (PBI), West Palm Beach, Florida, where one of the owners and two guests boarded the airplane. The pilot had the airplane topped off with fuel and visually confirmed a top-off of 22 gallons.
> 
> Preflight inspection, start, taxi, run-up and takeoff checks were normal, and the airplane departed PBI about 1015. The pilot climbed the airplane to 9,500 feet and landed at MYSM 2 hours later. Ground speeds were 184 to190 knots. Fuel tanks were switched inboard to outboard at the top of the climb and back to inboard prior to landing. Cruise power setting was 65 percent, 2,400 RPM and 27 inches of manifold pressure. Descent was a coupled, 400 fpm constant power down to 1,000 feet.
> 
> After unloading and clearing customs, the airplane took off for FPR about 1240. Pre-flight, start, taxi, run-up and pre-takeoff checks were "normal." The pilot noted a slight split in manifold pressure throughout the climb. By the time the airplane reached a cruising altitude of 10,500 feet, the left engine was unable to maintain more than 55 per cent power, 2,200 rpm and 26 inches of manifold pressure. The pilot matched the right engine power to that setting.
> 
> Fuel tanks were switched at the top of the climb. The pilot consulted the Pilot Operating Handbook which indicated a 4 gallon-per-hour reduction in fuel consumption. Ground speeds were 152 to160 knots. Estimated time en route per the GPS was 2.6 hours of total time.
> 
> The pilot utilized the outboard fuel tank fuel after reaching cruise altitude. The left outboard tank emptied about 15 minutes before the right tank, which was unusual as both engines burned evenly, and would [normally] lose power within 5 minutes of each other.
> 
> About 60 nm from FPR, the pilot started a coupled, 400-feet-per-minute (fpm) rate of descent. About 40 nm south of FPR, the left engine began surging. Fuel gauges indicated just below 1/4 full on the left main fuel tank and above 1/4 full on the right main fuel tank.
> 
> The pilot turned on the emergency boost pump, then selected fuel cross flow which restored power to the left engine. Using the "nearest airport" GPS function, he determined that PBI was the closest airport, 14 nm closer than FPR.
> 
> The airplane was slightly north of PBI at that point, so the pilot slowed the descent rate, turned the airplane toward PBI, contacted Palm Beach Approach Control and continued the descent. PBI was landing runways 10R, 10L, and 14.
> 
> The controller advised the pilot to cross the Palm Beach Inlet at 2,000 feet for runway 14.
> 
> Shortly thereafter, the left engine surged, then lost power, followed closely by the right engine. The pilot turned on the emergency boost pumps, switched to the outboard fuel tanks and inboard tanks sequentially, both separately and with cross flow, but was unable to restore engine power.
> 
> The pilot then completed the feathering procedure for both engines and established a best glide attitude. The airplane was about 7,500 feet at the time, with a descent rate of about 500 fpm.
> 
> The pilot considered his landing options, which included requesting runways 28R or 28L. He elected to remain on the heading for the inlet as it was doubtful that the airplane would make it all the way to the airport. Once past the beach, the flight path direct to the airport was over a densely populated area. As the airplane got closer, the options became the beach north of the inlet, the beach south of the inlet, or the water just offshore. There was a long, wide, clear spot on the southern beach adjacent to the inlet with no people on it.
> 
> The pilot advised the controller that a landing was assured on the beach south of the inlet. He established a high base turn over the inlet, completed the landing checks, selected full flaps and turned onto a final approach. Pumping the landing gear down was not an option, and the airplane touched down in a nose high attitude, decelerated rapidly, and spun counter-clockwise about 450 degrees. AIRCRAFT INFORMATIONAccording to the Piper Navajo Service Manual,
> 
> "The fuel system is contained in two independent systems that allow each engine to have its own fuel supply. The systems are connected by a cross feed valve that allows fuel to be drawn from one set of fuel cells to the engine on the opposite side, in the event of an emergency. The fuel cells are of the bladder type. The inboard cells (main) and the outboard cells (auxiliary) are installed in cavities in the wings. Each inboard cell has a capacity of 56 U.S. gallons and each outboard has a capacity of 40 U.S. gallons.
> 
> Fuel is taken from each cell through a screen located in the cell outlet fitting and then onto the shutoff selector valve. From the selector valve, fuel is drawn in a series configuration through the fuel filter, electric fuel pump, emergency shutoff valve and onto the engine-driven pump. These units, except for the engine driven pump, are accessible through a panel located between the underside of each wing and the fuselage.
> 
> The fuel filter, and electric and engine pumps incorporate a bypass that will open in the event of fuel stoppage through the normal passage. Drains are provided for each fuel cell, filter bowl and the cross feed line. The cell drains are visible on the underside of each wing at the inboard end of the cells. The filter bowl drains are accessible through an access door on the panel that is located between the underside of each wing and the fuselage. The cross feed is located on the left panel, aft of the filter bowl access door.
> 
> The fuel valves are operated through controls located in a panel just ahead of the main spar, between the pilot seats.
> 
> Fuel gauges will indicate the quantity of fuel in each cell that fuel is being drawn from." AIRPORT INFORMATIONAccording to the Piper Navajo Service Manual,
> 
> "The fuel system is contained in two independent systems that allow each engine to have its own fuel supply. The systems are connected by a cross feed valve that allows fuel to be drawn from one set of fuel cells to the engine on the opposite side, in the event of an emergency. The fuel cells are of the bladder type. The inboard cells (main) and the outboard cells (auxiliary) are installed in cavities in the wings. Each inboard cell has a capacity of 56 U.S. gallons and each outboard has a capacity of 40 U.S. gallons.
> 
> Fuel is taken from each cell through a screen located in the cell outlet fitting and then onto the shutoff selector valve. From the selector valve, fuel is drawn in a series configuration through the fuel filter, electric fuel pump, emergency shutoff valve and onto the engine-driven pump. These units, except for the engine driven pump, are accessible through a panel located between the underside of each wing and the fuselage.
> 
> The fuel filter, and electric and engine pumps incorporate a bypass that will open in the event of fuel stoppage through the normal passage. Drains are provided for each fuel cell, filter bowl and the cross feed line. The cell drains are visible on the underside of each wing at the inboard end of the cells. The filter bowl drains are accessible through an access door on the panel that is located between the underside of each wing and the fuselage. The cross feed is located on the left panel, aft of the filter bowl access door.
> 
> The fuel valves are operated through controls located in a panel just ahead of the main spar, between the pilot seats.
> 
> Fuel gauges will indicate the quantity of fuel in each cell that fuel is being drawn from." WRECKAGE AND IMPACT INFORMATIONAccording to a responding FAA inspector, the right engine firewall was substantially damaged, there was no fuel observed onboard, and there was no evidence of fuel leakage. There were also no apparent preexisting mechanical anomalies noted with the airplane other than the left engine turbocharger, which revealed evidence of oil seepage between the turbine and compressor sections.
> 
> FAA personnel were not present when the airplane was removed from the beach; however, the insurance adjuster who was present also did not note any evidence of fuel leakage on the underside of the airplane once it was lifted. Photographs confirmed no fuel streaks underneath.
> 
> A follow-on examination of the left engine turbocharger under FAA oversight did not reveal any defects with the unit.
> 
> The pilot did not note any preexisting anomalies with the fuel quantity indicators. ADDITIONAL INFORMATIONRadar data was requested from the FAA for the accident flight. However, the only data provided was from about the time that the pilot contacted Palm Beach Approach Control.
> 
> A commercial flight tracking web site, FlightAware, revealed outbound radar tracking from PBI to MYSM, with a takeoff time of 0957, and a landing time of 1206. However, there was no data available for the return flight.
> 
> A direct line plot from MYSM to FPR indicated that the airplane would have passed over Grand Bahama International Airport (MYGF), Freeport, The Bahamas. At the time the pilot called Palm Beach Approach Control, the airplane was about 50 nm beyond MYGF, 55 nm from FPR, and 32 nm northeast of PBI.
> 
> MYSM did not have fuel. According to multiple sources, MYGF had 100 LL fuel.
> 
> In a written statement, the pilot stated that he took off from MYSM at 1240. On the NTSB Pilot/Operator Report, he stated that he took off at 1220. A request to Bahamian authorities for an official takeoff time was unsuccessful.
> 
> The pilot also stated in the Pilot/Operator Report that the airplane took off from MYSM with 120 gallons of fuel onboard.
> 
> The pilot provided a copy of his flight planning calculations. According to his flight planning, start, taxi and run-up fuel usage was 12.0 gallons, two climbs combined for 15.6 gallons, 65 percent power cruise PBI to MYSM was 52.8 gallons, and MYSM to FPR 66.7 gallons for a total time of 4.6 hours and 147.1 gallons used.
> 
> The pilot also provided previous U.S. to/from The Bahamas fuel usage and noted that he had successfully flown the airplane round trip to MYSM on numerous previous occasions, with varying routes, with hours of operation ranging from 4.6 to 5.1 hours.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot’s in-flight misjudgment of fuel remaining resulting in fuel exhaustion and a total loss of engine power. Contributing to the accident was an inadequate fuel quantity for the flight for reasons that could not be determined during postaccident investigation.

- duplicate stripped finding descriptions in this event: **0**

---

## 17. `20190925X65544` — CEN19TA333

- date: `09/25/19 00:00:00`  year `2019`  type `ACC`
- location: Bolivar, MO USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Aircraft-Aircraft systems-Hydraulic power system-Reservoir, main-Not serviced/maintained | `C` | `0102291614` |
| 1 | 2 | `C` | `T` | Aircraft-Aircraft systems-Landing gear system-Gear extension and retract sys-Inoperative | `C` | `0102323026` |
| 1 | 3 | `F` | `T` | Personnel issues-Task performance-Maintenance-Scheduled/routine maintenance-Owner/builder | `F` | `0206201049` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 285 words

> On September 25, 2019, at 1335 central daylight time, a Lancair 320 airplane, N52WL, experience a landing gear system malfunction while on approach to Bolivar Municipal Airport (M17), Bolivar, Missouri. The private pilot was not injured, and the airplane sustained substantial damage to the right wing during the landing. The airplane was registered to and operated by the pilot as a Title 14 Code of Federal Regulations Part 91 personal flight. Visual meteorological conditions prevailed at the time of the accident, and a flight plan had not been filed. The airplane departed the Sparta/Fort McCoy Airport, Sparta, Wisconsin, at 1115, and was destined for M17.
> According to the pilot, while on visual approach to M17, he activated the landing gear extension switch and noticed the right main landing gear indication was not illuminated. The pilot recycled the landing gear, checked the landing gear circuit breaker, and performed an emergency landing gear extension; however, the right main landing gear did not extend. The pilot burned fuel for about 1 hour and landed on runway 18. During the landing, the right wing contacted the runway and terrain. The airplane came to rest upright. 
> Examination of the airplane by Federal Aviation Administration inspectors revealed the airplane hydraulic fluid reservoir contained a minimal amount of fluid (see Figure 1). No visual leaks were noted with the hydraulic system. The reservoir tank was located aft of the firewall and was not visible during a pre-flight inspection due to fuselage structure. The most recent condition inspection was completed on January 12, 2017. The pilot stated he knew the inspection was out of date and was working on getting the inspection completed.
> 
> Figure 1. Hydraulic Fluid Reservoir - Level Below Minimum (FAA)

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> Inadequate maintenance of the airplane, which resulted in a lack of adequate hydraulic fluid, malfunction of the landing gear extension system, and the landing gear collapse on landing.

- duplicate stripped finding descriptions in this event: **0**

---

## 18. `20170727X15642` — ANC17FA039

- date: `07/27/17 00:00:00`  year `2017`  type `ACC`
- location: Port Alsworth, AK USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Action/decision-Info processing/decision-Decision making/judgment-Pilot | `C` | `0204152044` |
| 1 | 2 | `C` | `T` | Personnel issues-Psychological-Perception/orientation/illusion-Situational awareness-Pilot | `C` | `0202203544` |
| 1 | 3 | `C` | `T` | Personnel issues-Psychological-Attention/monitoring-Monitoring environment-Pilot | `C` | `0202154544` |
| 1 | 4 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Altitude-Not attained/maintained | `C` | `0106201220` |
| 1 | 5 | `C` | `T` | Environmental issues-Conditions/weather/phenomena-Ceiling/visibility/precip-Below VFR minima-Decision related to condition | `C` | `0303507584` |
| 1 | 6 | `F` | `T` | Organizational issues-Management-Policy/procedure-Adequacy of policy/proc-Operator | `F` | `0402101569` |
| 1 | 7 | `F` | `T` | Organizational issues-Support/oversight/monitoring-Oversight-Oversight of operation-Operator | `F` | `0403201569` |
| 1 | 8 | `F` | `T` | Organizational issues-Support/oversight/monitoring-Oversight-Oversight of operation-FAA/Regulator | `F` | `0403201570` |
| 1 | 9 | `F` | `T` | Organizational issues-Management-Culture-Safety-Not specified | `F` | `0402401099` |
| 1 | 10 | `F` | `T` | Organizational issues-Management-Culture-Pressures/demands-Not specified | `F` | `0402402099` |
| 1 | 11 | `-` | `T` | Personnel issues-Task performance-Planning/preparation-Weather planning-Pilot | `-` | `0206102044` |
| 1 | 12 | `-` | `T` | Personnel issues-Task performance-Planning/preparation-Weather planning-Flt operations/dispatcher | `-` | `0206102038` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 5819 words

> HISTORY OF FLIGHTOn July 27, 2017, about 0923 Alaska daylight time, a wheel-equipped Cessna U206G airplane, N1749R, impacted remote, tree-covered terrain while en route to a remote lodge on the Mulchatna River, about 12 miles northeast of Port Alsworth, Alaska, in the Lake Clark National Park and Preserve. The commercial pilot and sole occupant sustained fatal injuries, and the airplane was destroyed by a postcrash fire. The airplane was registered to Laughlin Acquisitions, LLC, Anchorage, Alaska and was being operated by Alaska Skyways, Inc., dba Regal Air, Anchorage, Alaska as a Title 14 Code of Federal Regulations (CFR) Part 135 visual flight rules (VFR) on-demand cargo flight. Instrument meteorological conditions (IMC) were reported in the vicinity of the accident site at the time of the accident, and company flight following procedures were in effect. The flight originated from the Lake Hood Seaplane Base (LHD), Anchorage, Alaska, about 0800.
> 
> The operator reported that the purpose of the flight was to deliver 334 pounds of lumber and insulation to the Kautumn Lodge on the Mulchatna River, about 29 miles northeast of Koliganek, Alaska and would conclude with a return flight to LHD with three passengers onboard. The Kautumn Lodge is about 245 miles southwest of LHD. Upon leaving LHD and departing to the southwest, the route of flight consisted of tree-covered terrain. Continuing past Tyonek, Alaska to the southwest, is the south to north oriented mountainous terrain of the Alaska Range, which also encompasses the Lake Clark National Park and Preserve. Continuing past the Lake Clark National Park and Preserve to the southwest consists mainly of hills before reaching the Mulchatna River. 
> 
> The airplane was equipped with a Spidertracks Spider 6 system, which provided the operator real-time information such as location, direction, altitude, and airspeed of the airplane at 10-minute intervals. A review of the data showed that, before entering the Alaska Range, the airplane was at an altitude of 7,523 ft above mean sea level (msl) at 124 knots at 0839. The remaining three data points showed the airplane at 7,494 ft msl and 125 knots at 0849, 7,609 ft msl and 127 knots at 0859, and 3,954 ft msl and 135 knots at 0909. Figure 1 shows the various data points captured by the Spidertracks Spider 6 system.
> 
> 
> 
> Figure 1 – View of Spidertracks Spider 6 data points (courtesy of the operator).
> 
> 
> 
> The airplane was also equipped with an Automatic Dependent Surveillance – Broadcast (ADS-B) system. A review of ADS-B data showed the airplane departing LHD, traveling southwest toward the Alaska Range, and entering the airspace over the Lake Clark National Park and Preserve. The ADS-B data terminated about the same location as the second-to-last data point obtained from Spidertracks. Refer to the public docket for the Spidertracks and ADS-B data from the accident flight.
> 
> At 0924, the operator received a telephone call from the U.S. Air Force Alaska Rescue Coordination Center at Joint Base Elmendorf-Richardson, Alaska indicating a signal was received from the airplane's 406-MHz emergency locator transmitter (ELT). An aerial search mission was conducted with an airplane from the operator based at LHD, an airplane from the National Park Service based at Port Alsworth, and with a private helicopter based at Port Alsworth. The burning wreckage was discovered via aerial search in a forested area of the Miller Creek drainage about 1030. The wreckage was located about 85 miles northeast of the Kautumn Lodge. The location of the wreckage is shown in figure 2.
> 
> 
> 
> 
> 
> Figure 2 – Aerial view of the wreckage (courtesy of the NTSB).
>  PERSONNEL INFORMATIONPilot 
> 
> The operator's pilot training records showed no deficiencies and indicated that the pilot had completed all required training and was current, including a competency check ride on May 22, 2017. This was the pilot's first season working for the operator as a pilot and his first season as a pilot in Alaska. All his experience for the operator were based out of LHD as a dockhand for two summer seasons. The pilot was qualified and current to fly the wheel and float-equipped Cessna 206 and the float-equipped de Havilland DHC-2. The pilot completed all the operator's required initial training in early to mid-May 2017. According to the operator, at the time of the accident the pilot had 20 hours total of actual instrument experience and 84 hours total of simulated instrument experience. 
> 
> Director of Operations
> 
> The director of operations (DO), is listed in the Regal Air General Operations Manual (GOM) as the president and vice-president/secretary of the company. The DO is also the owner of the company. This was the DO's 18th year working for the company and was his 11th year working as a pilot and as the DO for the company. All his experience for the operator was based out of LHD. The DO was qualified and current to fly the wheel/ski/float-equipped Cessna 206, the wheel/ski/float-equipped de Havilland DHC-2, and the Piper PA-31-350. Prior to and at the time of the accident, the DO was out of the country on personal leave. 
> 
> Office Manager
> 
> The office manager had been employed for the operator for 8 years and first worked as a dockhand before becoming the office manager. While the office manager held a private pilot certificate (airplane single engine land), he had never flown for the operator nor for any other commercial operators in Alaska. He did not hold an aircraft dispatcher license, nor was he required to. All his experience for the operator was based out of LHD. The DO reported that the office manager, acting as the duty officer based out of the operator's headquarters at LHD, was the individual exercising operational control (first-tier with the two-tiered operational control concept) over the accident flight since he was out of the country on personal leave. The DO further reported that either himself or the office manager are the ones that exercise operational control over the company's flights. 
> 
> Principal Operations Inspector 
> 
> The principal operations inspector (POI), from the Federal Aviation Administration (FAA) Anchorage Flight Standards District Office, Anchorage, Alaska had been assigned to the operator's certificate since June 2016. The POI was an experienced air transport pilot and certificated flight instructor, with flight experience in Alaska, along with holding positions as a chief flight instructor (14 CFR Part 141 pilot school operations) and as a chief pilot (14 CFR Part 135 commuter and on-demand operations) prior to working for the FAA. 
>  AIRCRAFT INFORMATION
> Figure 3 – Exemplar photograph of N1749R (courtesy of the operator). 
> 
> 
> The airplane was configured for cargo operations at the time of the accident. A belly cargo pod was installed underneath the fuselage as shown in figure 3. The airplane was not equipped with a terrain awareness and warning system or onboard weather system, nor was it required to be. The airplane was not instrument flight rules equipped or certified, nor was it required to be.
>  METEOROLOGICAL INFORMATIONWeather Sources
> 
> The closest official weather observation station was located at Port Alsworth Airport (TPO), Port Alsworth, Alaska about 12 miles southwest of the accident site. The Aviation Routine Weather Report (commonly referred to as a "METAR") observation at 0650 (about 2.5 hours before the accident) included calm wind, 10 statute miles visibility, few clouds at 300 ft above ground level (agl), a broken ceiling at 1,500 ft agl, temperature 55°F, dew point 54°F, and an altimeter setting of 29.94 inches of mercury with remarks, "estimate pass closed" (the remark refers to the Lake Clark Pass). Figure 4 shows a National Weather Service (NWS) flying weather graphic issued at 0400 and was valid until 1000, showing the area encompassing the route of flight and the accident site as having forecast marginal VFR conditions. 
> 
> 
> 
> Figure 4 – View of National Weather Service flying weather graphic, issued at 0400 and valid until 1000 (courtesy of the National Weather Service).
> 
> 
> The following are images captured from a FAA weather camera station located at Lake Clark Pass West about 30 minutes before the pilot departed from LHD. These weather cameras are located about 10 miles east of the accident site and an elevation of 261 ft as shown in figure 5. Figure 6, figure 7, and figure 8 were taken prior to the pilot's departure from LHD and indicated complete mountain obscuration conditions with low visibility underneath the overcast cloud layer with all the higher terrain references obscured by clouds. 
> 
> 
> 
> 
> Figure 5 – Map of the closest FAA weather camera stations and the accident site (courtesy of the NTSB).
> 
> 
> 
> 
> Figure 6 – FAA weather camera image, Lake Clark Pass West – NorthEast, 0731 (courtesy of the FAA).
> 
> 
> 
> 
> Figure 7 – FAA weather camera image, Lake Clark Pass West – East, 0734 (courtesy of the FAA).
> 
> 
> 
> 
> Figure 8 – FAA weather camera image, Lake Clark Pass West – South, 0738 (courtesy of the FAA).
> 
> 
> The TPO METAR observation at 0958 (about 35 minutes after the accident) included calm wind, 15 statute miles visibility, a broken ceiling at 500 ft agl, overcast at 2,000 ft agl, temperature 57°F, dew point 55°F, altimeter 29.96 inches of mercury with remarks, "estimate pass closed" (the remark refers to the Lake Clark Pass).
> 
> Figure 9, figure 10, and figure 11 were captured from the FAA weather camera station located at Lake Clark Pass West, about the time of the accident. These three figures, similar to the images captured prior to the flight's departure, indicated complete mountain obscuration conditions with low visibility underneath the overcast cloud layer with all the higher terrain refences obscured by clouds. 
> 
> 
> 
> 
> 
> 
> Figure 9 – FAA weather camera image, Lake Clark Pass West – NorthEast, 0921 (courtesy of the FAA).
> 
> 
> 
> 
> 
> Figure 10 – FAA weather camera image, Lake Clark Pass West – East, 0926 (courtesy of the FAA).
> 
> 
> 
> 
> 
> Figure 11 – FAA weather camera image, Lake Clark Pass West – South, 0918 (courtesy of the FAA).
> 
> 
> A witness, who was a pilot and lived off Lake Clark near Port Alsworth reported that on the morning of the accident, conditions were "very foggy" with about ½ mile visibility until 0830 when the fog started to break up. He reported that by 0930, the sun was "breaking through" over Lake Clark. He departed for Anchorage in his airplane about 1000 and climbed to 4,500 ft over the fog and scattered clouds. He observed that there was still "quite a lot of fog" around which extended through Lake Clark Pass. He estimated that there was about a 300 ft ceiling under the fog in Lake Clark Pass. 
> 
> Accident Weather Flight Planning
> 
> No record was found of the pilot obtaining an official weather briefing from an FAA Flight Service Station or any Direct User Access Terminal Service (DUATS) before the flight. 
> 
> Prior to the flight departing, the office manager checked two sources of cameras. The office manager checked a private camera in a residential area of Port Alsworth and observed "bright blue sky." The office manager checked the FAA weather camera station located at Lake Clark Pass West and he noticed it had "some fog" but he reported, "it looked like it was just fog right over the camera because everywhere else was blue sky." The office manager also reviewed a weather report he received from the Kautumn Lodge that morning, with the destination reporting "great flying weather." The office manager reported that him and the pilot did not assess the METAR issued for TPO that morning prior to the flight departing.
> 
> The chief pilot reported that he also checked the weather at the time the pilot was conducting flight planning and did not notice any weather of concern. He further reported that, based on the weather information that he obtained, he felt that there were no weather conditions present for the flight that the pilot could not handle. 
> 
> Weather Flight Planning Procedures
> 
> FAA Operations Specification A010, Aviation Weather Information, stated that the operator was approved to use NWS for those United States and its territories located outside of the 48 contiguous States, and an Enhanced Weather Information System to obtain and disseminate aviation weather information for the control of flight operations.
> 
> The Regal Air GOM discussed weather planning procedures for company pilots and stated that, before the flight to each new destination, the pilot will use whatever means he/she deems appropriate for obtaining current weather, including FAA Flight Service, DUATS or National Oceanic and Atmospheric Administration websites, or calling the destination for a current analysis of the weather. The GOM stated that the decision to embark on a flight was at the discretion of the PIC should poor weather exist; but that no flight was to be flown in weather below federal aviation regulations allowable minimums.
> 
> The Regal Air GOM did not require pilots or individuals in operational control roles to receive an official weather briefing; nor was there any requirement for the individual exercising operational control and the pilot to jointly assess current or forecast weather conditions for a flight.
> 
> FAA Advisory Circular (AC) 00-45H Aviation Weather Services discusses weather briefings and states in part:
> 
> 
> Prior to every flight, pilots should gather all information vital to the nature of the flight. This includes a weather briefing obtained by the pilot from an approved weather source, via the Internet, and/or from an flight service station (FSS) specialist. 
> 
> 
> Refer to the NTSB Weather Study in the public docket for additional information.
>  AIRPORT INFORMATION
> Figure 3 – Exemplar photograph of N1749R (courtesy of the operator). 
> 
> 
> The airplane was configured for cargo operations at the time of the accident. A belly cargo pod was installed underneath the fuselage as shown in figure 3. The airplane was not equipped with a terrain awareness and warning system or onboard weather system, nor was it required to be. The airplane was not instrument flight rules equipped or certified, nor was it required to be.
>  WRECKAGE AND IMPACT INFORMATIONOn July 28, 2017 the NTSB investigator-in-charge (IIC), an aviation safety inspector from the FAA Polaris Certificate Management Office, and the Alaska State Troopers traveled to the accident site via helicopter. The team members hiked into the accident site to conduct wreckage documentation. The accident site, about 920 ft above mean sea level, was in a forested valley, surrounded by steep, mountainous terrain. The accident site was about ¼-mile southeast of the Kijik River. The average tree height, consisting of both spruce and birch trees, at the accident site was about 35 feet tall. All of the components of the airplane were found at the main wreckage site.
> 
> 
> 
> Figure 12 – View of the front side of the wreckage (courtesy of the NTSB).
> 
> 
> The airplane came to rest in a wings-level attitude on a magnetic heading about 100° as shown in figure 11. Portions of broken windscreen, the magnetic compass, and the Spidertracks unit were scattered forward of the wreckage. The wreckage aft of the firewall, extending outboard to both wing roots and to the mid-empennage area, was destroyed by fire. 
> 
> The leading edges of both wings appeared relatively intact. The left wing tip was separated and found lying on the leading edge of the left wing. The right wing tip (along with the right wing tip light assembly) was separated and found about 17 ft from the right wing on a 200° heading. The outboard section of the right wing was separated and found about 8 ft forward of the right wing on a 180° heading and displayed impact damage.
> 
> Both fuel tanks were compromised by fire damage and no fuel was observed. The lower portion of the engine was buried in dirt. The top portion of the engine exhibited no signs of fluid leaks or pre-impact damage. The propeller blades exhibited varying degrees of impact damage. The propeller was attached to the crankshaft flange. The 406-MHz ELT was found just aft of the mid-empennage burn section and displayed heavy fire damage. 
> 
> The wreckage was recovered from the accident site and transported to a secure facility in Wasilla, Alaska, for further examination. On October 5, 2017, a wreckage examination and layout were conducted under the direction of the NTSB IIC. Representatives from the FAA, Textron Aviation, Continental Motors, and Regal Air were also present. The examination revealed no preimpact mechanical malfunctions or failures with the airframe and engine. 
>  ADDITIONAL INFORMATIONControlled Flight Into Terrain 
> 
> FAA AC 61-134 General Aviation Controlled Flight Into Terrain Awareness discusses the risk that controlled flight into terrain (CFIT) poses for pilots and states in part:
> 
> 
> Operating in marginal VFR/IMC conditions is more commonly known as scud running.
> 
> 
> The importance of complete weather information, understanding the significance of the weather information, and being able to correlate the pilot's skills and training, aircraft capabilities, and operating environment with an accurate forecast cannot be emphasized enough.
> 
> Controlled Flight Into Terrain-Avoidance Training Program
> 
> While 14 CFR Part 135 helicopter operators are required to have a controlled flight into terrain-avoidance (CFIT-A) training program, 14 CFR Part 135 airplane operators are not required to have such a program.
> 
> Aviation Weather and Risk Taking
> 
> NTSB safety study, Aviation Safety in Alaska SS-95/03, discusses aviation safety issues regarding weather and risk taking in Alaska and states, in part:
> 
> Flying weather in Alaska can be quite variable depending on the climate zone and time of year. Although all parts of Alaska experience periods of instrument meteorological conditions, such conditions are frequent in the Aleutian Islands, Alaska Peninsula, southeast Alaska, and the Arctic Coast during the summer and early fall. Weather conditions can change rapidly in Alaska, and the vast distances between some reporting points will often conceal significant local variations in the weather. VFR flight into IMC usually involves poor pilot decision making, whether in initiating the flight or continuing it into adverse weather.
> 
> VFR into IMC Accidents
> 
> The FAA's report, A Human Factors Analysis of Fatal and Serious Injury Accidents in Alaska 2004-2009, discusses five factors associated with poor pilot decision-making in VFR into IMC accidents and states, in part:
> 
> Weigmann and Goh (2000) list four factors associated with poor pilot decision-making in VFR into IMC accidents.
> 
> The first factor is poor situation assessment. The pilot lacks experience in interpreting changing weather conditions, especially slowly changing weather. Tiredness, fatigue, and increased workload, or some combination of these, can also increase the likelihood of an inaccurate assessment of the weather.
> 
> The second factor associated with poor pilot decision-making is faulty risk perception of the dangers involved in flying in marginal weather conditions. Recent research by Shappell et al. (2010) supports the notion that many pilots have a poor understanding and appreciation of the hazards associated with adverse weather conditions. Contributing to this perception, many pilots might have successfully navigated during marginal conditions in the past and so have gained confidence in their ability to succeed again in similar circumstances. 
> 
> The third factor associated with poor pilot decision-making is inappropriate motivations that bias the decision-making process. The term "get-home-itis" refers to the motivation of the pilot to complete the journey.
> 
> The fourth factor associated with poor pilot decision-making is called "decision framing." Decision framing refers to the idea that a person's choice between a risky or safe course of action depends on whether the choice is framed in terms of a gain or a loss. When the safer course of action is framed in terms of a loss, the decision tends to be risk-seeking. When framed in terms of a gain, the decision tends to be risk-averse. In the case of VFR flight into IMC, research has shown that framing the decision to not fly into marginal weather conditions as a loss (i.e., wasted time, money, and effort) leads to a greater likelihood of continuing the flight, but framing the decision to not fly as a gain (i.e., it is safer) leads to a greater likelihood of diverting the flight (O'Hare & Smitheram, 1995).
> 
> A fifth factor, one that is not discussed by Weigmann and Goh, is what is referred to as problem- solving set (Gick & Holyoak, 1979), which is the tendency to repeat a solution process that has been previously successful. In addition to altering one's perception of risk, successfully conducting a flight in marginal conditions by using a specific strategy (e.g., following a river while flying underneath the clouds) will increase the likelihood that the strategy will be used again under similar circumstances. Memory plays a crucial role in problem-solving, and repetition plays a crucial role in memory. So when faced with a problem (how do I make it through this weather?), humans tend to adopt a strategy that has been used successfully in the past, even if the current situation does not quite match previous events.
> 
> Flight Risk Assessment Tool Benefits 
> 
> The FAA Safety Team (FAASTeam) document, Flight Risk Assessment Tools (General Aviation Joint Steering Committee Safety Enhancement Topic SE 42), explains the multiple benefits of using a FRAT and states in part:
> 
> "In the thick" is no time to try to mitigate a potentially hazardous outcome. When preparing for a flight or maintenance task, operators and maintenance technicians should take time to stop and think about the hazards involved. 
> 
> 
> Attempting this task "in our heads" usually does not take into account actual risk exposure. The mind tends to compartmentalize the individual hazards which, in turn, fails to appreciate their cumulative effects. We may also allow our personal desires to manipulate our risk assessment in order to meet personal goals. The best way to compensate for these inherent shortcomings is to take the task to paper. 
> 
> 
> Putting everything on "paper" allows us to establish our risk limits in an atmosphere free from the pressure of an impending flight or maintenance task. It also gives a perspective on the entire risk picture that we cannot get in our heads. More importantly, it sets the stage for managing risk through proactive risk mitigation strategies that are documented.
> 
> 
> Decision Making
> 
> A Human Error Approach to Aviation Accident Analysis: The Human Factors Analysis and Classification System by Douglas Weigmann and Scott Shappell discusses preconditions for unsafe acts. This book discusses decision errors by members of an organization and states in part:
> 
> Decision errors, represents intentional behavior that proceeds as planned, yet the plan itself proves inadequate or inappropriate for the situation. Often referred to as "honest mistakes," these unsafe acts represent the actions or inactions of individuals whose "hearts are in the right place," but they either did not have the appropriate knowledge or just simply chose poorly. 
> 
> Alaska Bush Syndrome
> 
> NTSB's safety study, Aviation Safety in Alaska SS-95/03, identifies and discusses what is known as the bush syndrome that affects aviation operations in Alaska. This document states that the bush syndrome is defined as an attitude of air taxi operators, pilots, and passengers ranging from their casual acceptance of risks to their willingness to take unwarranted risks. This document further states:
> 
> The demands for reliable air service in Alaska can easily place pressures on pilots and operators to perform. An underlying factor in risk-taking, or "bush syndrome," is a response by pilots and operators to powerful demands for reliable air service in an operating environment and aviation infrastructure that are often inconsistent with those demands. 
>  FLIGHT RECORDERSThe airplane did not carry, nor was required to carry, a crashworthy flight data recorder. At the time of the accident, the operator did not have formal flight data monitoring program in place, nor was it required to have one.
>  MEDICAL AND PATHOLOGICAL INFORMATIONThe Alaska State Medical Examiner, Anchorage, Alaska conducted an autopsy of the pilot. The cause of death was attributed to multiple blunt force injuries with a contributing cause of thermal injuries.
> 
> The FAA's Bioaeronautical Research Sciences Laboratory, Oklahoma City, Oklahoma, performed toxicology tests on specimens from the pilot; results were negative for ethanol and drugs. Carbon monoxide and cyanide tests were not performed. 
>  ORGANIZATIONAL AND MANAGEMENT INFORMATIONAt the time of the accident, Regal Air was headquartered at LHD and conducted cargo, charter, and sightseeing flights throughout Alaska. The operator's fleet comprised wheel-, ski-, and float-equipped Cessna 206s; wheel-, ski-, and float-equipped de Havilland DHC-2s; and a Piper PA-31-350. 
> 
> Operational Control
> 
> The Regal Air GOM discussed operational control and stated in part:
> 
> Operational Control is defined in FAR 1 as "the exercise of authority over initiating, conducting, and terminating a flight". Operational Control is exercised through both active and passive means. Passive control consists of developing and publishing policies and procedures for operational control personnel and flight crews to follow in the performance of their duties and assuring adequate information and facilities are available to conduct the planned operation. Active control consists of making those decisions and performing those actions necessary to operate a specific flight such as crew scheduling, accepting charter flights from the public, reviewing weather and NOTAMs, and flight planning.
> 
> This document further stated that the president, DO, chief pilot, director of maintenance, the pilot in command, and the duty officer were authorized to act for Regal Air and exercise operational control under 14 CFR Part 135.77. The Regal Air GOM contains the individual names of company management personnel (DO, chief pilot, and director of maintenance). 
> 
> The duties and responsibilities listed for the duty officer, who reported to the DO, included keeping the daily flight log updated and accurate and handling flight following with the company flight plan. According to the GOM, the duty officer "may be any company officer, management personnel, or employee."
> 
> FAA Operations Specification A006 Management Personnel (commonly referred to as an "OpSpec"), included the 14 CFR Part 119 position title, name, and company equivalent position title at the time of the accident (DO, chief pilot, and director of maintenance) for Regal Air.
> 
> FAA Operations Specification A008, Operational Control, stated that, before conducting a Part 135 flight or series of flights, at least one management person listed in operations specification A006, Management Personnel, or a designee who was a direct employee of the certificate holder other than a pilot assigned to the specific flight or series of flights, was required to determine and be knowledgeable regarding several aspects of the flight, including whether the assigned crewmember was qualified and eligible to serve as a required crewmember in the aircraft and type of operation assigned and whether the aircraft assigned for use was listed in operations specification D085 and airworthy under the certificate holder's FAA-approved maintenance, inspection, or airworthiness program.
> 
> Additionally, it stated that, before conducting a Part 135 flight or series of flights, at least the pilot assigned to the flight was required to determine whether the flight could be initiated, conducted, or terminated safely and in accordance with the certificate holder's operations specifications, GOM, and/or appropriate regulations. This determination could be made by the assigned pilot or assigned flight crewmembers.
> 
> Non-management personnel exercising operational control were to meet the requirements of 14 CFR Part 119.69 (d) and 14 CFR Part 135.77. Their names, titles, duties, responsibilities, and authorities were to be specified within the GOM. 
> 
> 14 CFR Part 119.69 states that anyone in a position to exercise control over operations conducted under the operating certificate must be qualified through training, experience, and expertise; to the extent of their responsibilities have a full understanding of aviation safety standards and safe operating practices, Federal Aviation Regulations, the certificate holder's operations specifications, appropriate maintenance and airworthiness requirements, and Part 135 manual; and must perform their duties in order to meet legal requirements and maintain safe operations. 
> 
> 14 CFR Part 135.77, which addresses responsibility for operational control, states that each certificate holder is responsible for operational control and shall list, in the manual required for 14 CFR Part 135.21, the name and title of each person authorized by it to exercise operational control. 
> 
> Operational Control Training
> 
> The DO reported that the company did not have an operational control training program in place before the accident, nor were they required to. The NTSB issued Safety Recommendation A-17-039 to the FAA, which asked the FAA to, "Establish minimum initial and recurrent training requirements for personnel authorized to exercise operational control, including, but not limited to, approved subject knowledge areas, training hours, subject hours, and qualification modules." 
> 
> The FAA responded to the NTSB on July 21, 2017, and stated, "The FAA agrees that guidance for terrain avoidance can be expanded to include fixed-wing operations and to emphasize the importance of operational control. However, because this operational control change would require rulemaking, we intend to evaluate our current guidance, regulations, and policy, for part 135 operators to determine potential options to satisfy these safety recommendations." At the time of writing of this accident report, the status of Safety Recommendation A-17-039 is classified as "Open-Acceptable Response." Refer to the NTSB internet website for Safety Recommendation A-17-039.
> 
> Safety Management System
> 
> At the time of the accident, Regal Air had a formal safety management system (SMS) in place. The SMS was managed by the operator's aviation safety officer, who was the company president/director of operations and owner. The SMS includes a safety management plan, incident management, safety meetings, an emergency response plan, and safety education for employees. 
> 
> When asked if the company used any electronic flight risk assessment tools, the president/director of operations reported, "absolutely not, I can't stand them" and, "they're a complete waste of time."
> 
> FAA Order 8900.1 Flight Standards Information Management System
> 
> The FAA's Order 8900.1 Flight Standards Information Management System discusses the two-tiered operational control concept and states in part:
> 
> All first-tier actions must be taken by the certificate holder's direct employees. The first tier is the assignment of flightcrew member(s) and aircraft for revenue service under the operating certificate. The assignment of crew and release of aircraft to revenue service is the responsibility of the certificate holder, and must be made by the management of the certificate holder or management delegates. In order to be delegated the authority to make these decisions, the management delegates must be trained, found competent, and designated by the certificate holder, be listed in the GOM (or in OpSpec A006, A039 or A040, if applicable), and be under management supervision. . Management supervision means, for example, that the certificate holder tracks the actions of the management delegate or employee, samples the work of that employee (reviews a sample of the decisions made), and has the ability to enforce the certificate holder's standards through corrective actions such as retraining, requalification, or disciplinary actions such as disqualification, demotion, suspension, or termination. Because the certificate holder is responsible for the conduct of its employees or agents, it must have the ability to monitor and control their performance.
> 
> All second-tier actions may be taken either by the certificate holder's direct employees or by the certificate holder's agents. The second tier of operational control is more tactical. This involves the decisions made by personnel (such as the PIC) in the day-to-day conduct of operations. This may include the initiation of flights upon the PIC receiving a request from the customer directly (often the case in on-demand operations being conducted under a dedicated service contract, such as offshore operations or emergency medical service (EMS)). This is acceptable if the PIC is authorized by the certificate holder to make those decisions on behalf of the certificate holder. To do so would require that the PIC be trained, found competent by the certificate holder, designated, be listed in the GOM (or in OpSpec A006, A039, or A040, if applicable), and be under management supervision.
> 
> The GOM (or other appropriate documentation) must contain guidance which describes the certificate holder's operational control system. The training program must provide the certificate holder's personnel with the knowledge and skills required to ensure that the operational control system is effective.
> 
> The FAA's Order 8900.1 Flight Standards Information Management System, also identifies the three failure modes of operational control and states in part:
> 
> 1) Loss of operational control within the air carrier—hands-off management results in inadequate controls over its own operations.
> 
> 2) Loss of operational control within the air carrier—exercise of operational control by an unapproved person.
> 
> 3) Loss or surrender of operational control externally (e.g., an air carrier's illegal renting/franchising-out the use of its air carrier certificate to one or more uncertificated entities).
> 
> This document further summarizes operational control and states in part:
> 
> Only approved persons may exercise operational control on the certificate holder's behalf. The certificate holder must have adequate controls in place to ensure that officials in a position of authority over flights conducted under the certificate do so safely, and in compliance with the regulations, OpSpecs, GOM, as applicable, and accepted or approved procedures. Management of operations should never be inattentive, distracted, or careless. Hands-off management is not a legitimate excuse for failing to maintain operational control.
> 
> FAA Oversight and Surveillance
> 
> FAA Order 8900.1 Flight Standards Information Management System, discusses surveillance of operators, and states in part:
> 
> The Federal Aviation Administration (FAA) is empowered, by statutory requirement, "...to carry out the functions, powers, and duties of the Secretary relating to aviation safety." One of the most significant duties of the FAA is to conduct surveillance in all areas of air transportation safety. Surveillance is a continuing duty and responsibility of all aviation safety inspectors in the flight standards organization. The term "surveillance," as used in this handbook, relates to this ongoing duty and responsibility and related programs. Surveillance programs provide the FAA with a method for the continual evaluation of operator compliance with Title 14 of the Code of Federal Regulations (14 CFR) and safe operating practices. Information generated from the surveillance programs permits the FAA to act upon deficiencies, which affect or have a potential effect on aviation safety. For surveillance programs to be effective, they must be carefully planned and executed during the conduct of specific inspection activity. Inspections provide specific data, which can be further evaluated; therefore, they support and maintain ongoing surveillance programs.
> 
> Regal Air was managed by a certificate management team (CMT) based out of the Anchorage Flight Standards District Office. The CMT comprised one POI, one principal maintenance inspector, and one principal avionics inspector. Regal Air's FAA Operations Specifications were issued by the FAA. Regal Air's GOM was accepted by the FAA. Regal Air's training program was approved by the FAA.
> 
> During a postaccident interview, the POI stated that, at the time of the accident, he was responsible for surveilling a total of 50 certificates. He reported that this was the maximum number of certificates he had been assigned during his career. When asked if he felt he had adequate time to perform the duties associated with the 50 certificates, he responded that he did not, and that the workload was prioritized by risk for each certificate. A complete transcript of the interview is available in the public docket. 
> 
> Review of FAA records for Regal Air, which included data from Program Tracking and Reporting System (PTRS) and the Safety Assurance System (SAS), indicated that the POI conducted a GOM inspection on June 29, 2016, and no issues were noted. Additionally, no issues of concern were found noted in the PTRS and SAS data regarding Regal Air's operational control, flight release, or training programs during the 3 years before the accident.

- conclusion-term hits in factual narrative: `['contributing to', 'the cause of']`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's decision to continue visual flight into an area of instrument meteorological conditions, which resulted in a loss of visual reference and subsequent controlled flight into terrain. Contributing to the accident was (1) the inadequate preflight weather planning by the pilot and duty officer (2) the operator's inadequate operational control structure, and (3) the inadequate oversight of the operator's operational control structure by the Federal Aviation Administration.

- duplicate stripped finding descriptions in this event: **0**

---

## 19. `20150514X71721` — ANC15CA025

- date: `05/14/15 00:00:00`  year `2015`  type `ACC`
- location: Anchorage, AK USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 2 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Surface speed/braking-Incorrect use/operation | `C` | `0106204511` |
| 1 | 3 | `F` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Directional control-Not attained/maintained | `F` | `0106202020` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 88 words

> The pilot was on a personal flight in a tailwheel-equipped, single engine airplane. The pilot stated that after landing, and while taxiing to exit the runway, the airplane began to veer to the right. He applied the brakes in an effort to regain control and the airplane nosed over and came to rest inverted, resulting is substantial damage to the wings and fuselage. The pilot and sole occupant sustained minor injuries. The pilot stated there were no preaccident mechanical malfunctions or anomalies that would have precluded normal operation.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's excessive use of brakes to maintain directional control, which resulted in a nose over.

- duplicate stripped finding descriptions in this event: **0**

---

## 20. `20080714X01041` — LAX08CA189

- date: `06/24/08 00:00:00`  year `2008`  type `ACC`
- location: Laramie, WY USA
- Aircraft_Key values in findings: `[1]`

### Findings (model sees only the stripped text)

| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |
|---:|---:|:---:|:---:|---|:---:|---|
| 1 | 1 | `C` | `T` | Aircraft-Aircraft oper/perf/capability-Performance/control parameters-Airspeed-Not attained/maintained | `C` | `0106201020` |
| 1 | 2 | `C` | `T` | Personnel issues-Task performance-Use of equip/info-Aircraft control-Pilot | `C` | `0206304044` |
| 1 | 3 | `F` | `T` | Environmental issues-Conditions/weather/phenomena-Wind-Tailwind-Not specified | `F` | `0303401599` |
| 1 | 4 | `-` | `F` | Environmental issues-Physical environment-Object/animal/substance-Runway/taxi/approach light-Contributed to outcome | `-` | `0302201291` |

### Aircraft_Key 1 — `narr_accp` FACTUAL NARRATIVE (model-visible), 203 words

> In a written statement, the pilot reported that he performed a normal landing approach to runway 12 at Laramie Regional Airport.  As the airplane entered the traffic pattern, the pilot indicated he was a little high, but at pattern altitude as he came abeam the runway approach end.  Upon turning to final approach, he added the final flaps.  He was on the glide path at the normal airspeed and crossed over the runway numbers at 77 knots.  The airplane floated as he began the flare, and he noticed that the ground speed was very fast. The pilot continued the flare "as normal" when the stall warning horn sounded.  He looked down and saw that the airplane was about 10 to 15 feet above the runway.  He applied full power and right rudder to perform a go-around, but the airplane did not climb as expected and drifted to the left. He also added right aileron control inputs to maintain airplane control, but there were no positive results from the manipulation of the aileron. The airplane continued to descend, and the left wing touched the ground and hit a taxiway light. The airplane exited the runway and impacted the ground before coming to rest upright.

- conclusion-term hits in factual narrative: `[]`

### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)

> The pilot's failure to attain and maintain an adequate airspeed during a go around, that resulted in a stall/mush. Contributing to the accident was the tailwind condition.

- duplicate stripped finding descriptions in this event: **0**

---
