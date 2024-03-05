examples = [
    {
    
            "input": "What is the total count of shg?",
            "sql_cmd": """SELECT COUNT(DISTINCT c.cbo_id) AS shg_count 
                            FROM m_cbo c 
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id 
                            WHERE upper(t.type_short_name) = 'SHG' AND c.record_status=1""",
            "result": "[(1075033)]",
            "answer": "There are total 1075033 SHG ",

},
{
    "input": "What is the total count of CLF?",
            "sql_cmd": """SELECT COUNT(DISTINCT c.cbo_id) AS clf_count 
                            FROM m_cbo c 
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id 
                            WHERE upper(t.type_short_name) = 'CLF' AND c.record_status=1""",
            "result": "[(1658)]",
            "answer": "There are total 1658 CLF",
},


{
    "input": "What is the total count of VO?",
            "sql_cmd": """SELECT COUNT(DISTINCT c.cbo_id) AS vo_count \
                            FROM m_cbo c \
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id \
                            WHERE upper(t.type_short_name) = 'VO' AND c.record_status=1""",
            "result": """[(75368)]""",
            "answer": """There are total 75368 VO""",
},
{
            "input": "Number of cbo per block per district",
            "sql_cmd": """SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos \
                        FROM m_cbo c \
                        INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID \
                        INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID \
                        WHERE c.record_status=1 \
                        GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME""",
            "result": """ARARIA	Palasi	3410
                            ARARIA	Sikti	2330
                            BANKA	Katoria	2673
                            BANKA	Shambhuganj	2302
                            BEGUSARAI	Sahebpur Kamal	2057
                            BEGUSARAI	Teghra	1972
                            BEGUSARAI	Naokothi	1407
                            BHAGALPUR	Naugachhia	1605
                            BHOJPUR	Sahar	1207
                            BHOJPUR	Charpokhari	1190
                            BHOJPUR	Garhani	1044
                            BUXAR	Barhampur	1903""",
            "answer": """ARARIA	Palasi	3410
                            ARARIA	Sikti	2330
                            BANKA	Katoria	2673
                            BANKA	Shambhuganj	2302
                            BEGUSARAI	Sahebpur Kamal	2057
                            BEGUSARAI	Teghra	1972
                            BEGUSARAI	Naokothi	1407
                            BHAGALPUR	Naugachhia	1605
                            BHOJPUR	Sahar	1207
                            BHOJPUR	Charpokhari	1190
                            BHOJPUR	Garhani	1044
                            BUXAR	Barhampur	1903""",
        },
        
        {
            "input": "total count of 9 month old shg saving account",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS shg_count
FROM m_cbo c
INNER JOIN m_district d ON d.district_id = c.district_id
WHERE c.record_status = 1
AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG')
AND c.formation_date <= CURRENT_DATE - INTERVAL '9 MONTH'
AND c.formation_date > CURRENT_DATE - INTERVAL '10 MONTH'""",
            "result": """[(2110)]""",
            "answer": """2110 are count of 9 month old shg saving account""",
        },
        {
            "input": "total count of shg in project nrlm in current year",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_block b ON b.block_id = c.block_id
                        WHERE upper(b.project_code) = 'NRLM' 
                        AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG')
                        AND EXTRACT(YEAR FROM c.formation_date) = EXTRACT(YEAR FROM SYSDATE)
                        AND c.record_status=1""",
            "result": """[(32)]""",
            "answer": """There are total 32 SHG in project NRLM in current year""",
        },
        {
            "input": "how many clf are in NRETP project",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS clf_count
                        FROM m_cbo c
                        INNER JOIN m_block b ON b.block_id = c.block_id
                        WHERE upper(b.project_code) = 'NRETP' 
                        AND c.cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name)= 'CLF')
                        AND c.record_status=1""",
            "result": """[(306)]""",
            "answer": """There are total 306 CLF in project NRETP """,
        },
        {
            "input": "how many shg, vo and clf in district bhojpur",
            "sql_cmd": """SELECT
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'SHG') THEN 1 ELSE 0 END) AS shg_count,
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'VO') THEN 1 ELSE 0 END) AS vo_count,
                SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'CLF') THEN 1 ELSE 0 END) AS clf_count
                FROM m_cbo c
                WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'BHOJPUR')
                AND c.record_status=1""",
            "result": """[(20863	1535	37)]""",
            "answer": """There are total 20863 shg	1535 vo and	37 CLF in district BHOJPUR """,
        },
        {
             "input": "What is the count of all members across SHGs, VOs and CLFs in district Patna?",
            "sql_cmd": """SSELECT
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name)= 'SHG') THEN 1 ELSE 0 END) AS shg_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'VO') THEN 1 ELSE 0 END) AS vo_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE upper(type_short_name) = 'CLF') THEN 1 ELSE 0 END) AS clf_count
FROM m_cbo c
WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'PATNA')
AND c.record_status = 1""",
            "result": """[(41010	2725	65)]""",
            "answer": """There are total 41010 shg	12725 vo and	65 CLF in district PATNA """,
        },
        {
            "input": "how many shg saving account in last 6 months?",
            "sql_cmd": """SELECT
                    COUNT(DISTINCT c.CBO_ID) AS SHG_Saving_ACC
                FROM
                    M_CBO c
                JOIN
                    T_CBO_APPL_MAPPING cam ON c.CBO_ID = cam.CBO_ID
                JOIN
                    T_BULK_BANK_ACC bba ON cam.APPLICATION_ID = bba.APPLICATION_ID
                JOIN
                    M_CBO_TYPE ct ON c.CBO_TYPE_ID = ct.CBO_TYPE_ID
                WHERE
                    bba.ACC_TYPE_ID = 1
                    AND upper(ct.TYPE_SHORT_NAME) = 'SHG'
                    AND c.RECORD_STATUS = 1
                    AND cam.ACC_OPENING_STATUS = 2
                    AND bba.APPLICATION_DATE >= CURRENT_DATE - INTERVAL '6 MONTH'""",
            "result": """[(11083)]""",
            "answer": """There are total 11083 shg saving account in last 6 months """,
        },
        {
            "input": "how many shg saving account, vo saving account, clf saving account in last 6 month",
            "sql_cmd": """SELECT
                    SUM(CASE WHEN upper(ct.TYPE_SHORT_NAME) = 'SHG' THEN 1 ELSE 0 END) AS SHG_Saving_Accounts,
                    SUM(CASE WHEN upper(ct.TYPE_SHORT_NAME) = 'VO' THEN 1 ELSE 0 END) AS VO_Saving_Accounts,
                    SUM(CASE WHEN upper(ct.TYPE_SHORT_NAME) = 'CLF' THEN 1 ELSE 0 END) AS CLF_Saving_Accounts
                FROM
                    M_CBO c
                JOIN
                    T_CBO_APPL_MAPPING cam ON c.CBO_ID = cam.CBO_ID
                JOIN
                    T_BULK_BANK_ACC bba ON cam.APPLICATION_ID = bba.APPLICATION_ID
                JOIN
                    M_CBO_TYPE ct ON c.CBO_TYPE_ID = ct.CBO_TYPE_ID
                WHERE
                    bba.ACC_TYPE_ID = 1
                    AND c.RECORD_STATUS = 1
                    AND cam.ACC_OPENING_STATUS = 2
                    AND bba.APPLICATION_DATE >= CURRENT_DATE - INTERVAL '6 MONTH'""",
            "result": """[(11218	936	25)]""",
            "answer": """There are total 11218 shg_saving_account 936 VO_Saving_Accounts and 25 CLF_Saving_Accounts in last 6 months""",
        },
        {
            "input": "total count of shg in district patna in year 2023",
            "sql_cmd": """SELECT COUNT(c.CBO_ID) AS shg_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID  
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'SHG' 
                            AND upper(d.DISTRICT_NAME) = 'PATNA' AND EXTRACT(YEAR FROM c.formation_date) = 2023
                            AND c.record_status=1""",
            "result": """[(1286)]""",
            "answer": """1286 SHG were formed in district Patna in 2023""",
        },
        {
            "input": "total count of members in district patna and darbhanga",
            "sql_cmd": """SELECT d.DISTRICT_NAME, COUNT(cm.MEMBER_ID) AS member_count
                           FROM m_district d 
                           INNER JOIN m_cbo_member cm ON  cm.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(d.DISTRICT_NAME) IN ('PATNA', 'DARBHANGA')
                            AND cm.record_status=1
                            GROUP BY d.DISTRICT_NAME""",
            "result": """[(DARBHANGA	526984
                            PATNA	493022)]""",
            "answer": """there are 526984 members in Darbhanga and 493022 members in Patna""",
        },
        {
            "input": "total count of vo in december 2023",
            "sql_cmd": """SELECT 
                            COUNT(cbo_id) AS vo_count
                            FROM 
                            m_cbo c
                            INNER JOIN 
                            m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                            WHERE
                            upper(t.type_short_name) = 'VO'
                            AND EXTRACT(YEAR FROM c.formation_date) = 2023
                            AND EXTRACT(MONTH FROM c.formation_date) = 12
                            AND c.record_status=1""",
            "result": """[(81)]""",
            "answer": """total 81 vo were formed in december 2023""",
        },
        {
            "input": "What is the total number of VOs in Samastipur district?",
            "sql_cmd": """SELECT COUNT(c.CBO_ID) AS total_vos
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'VO' AND upper(d.DISTRICT_NAME) = 'SAMASTIPUR'
                            AND c.record_status=1
""",
            "result": """[(3402)]""",
            "answer": """there are 3402 VOs in Samastipur district"""
        },
        {
            "input": "How many SHGs  in Patna district formed between Jan to March 2023?",
            "sql_cmd": """SELECT
                        COUNT(*) AS shg_count  
                        FROM 
                        m_cbo c
                        INNER JOIN
                        m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                        INNER JOIN 
                        m_district d ON c.district_id = d.district_id
                        WHERE
                        upper(t.type_short_name) = 'SHG'
                        AND upper(d.district_name)= 'PATNA' 
                        AND EXTRACT(MONTH FROM c.formation_date) BETWEEN 1 AND 3 
                        AND EXTRACT(YEAR FROM c.formation_date) = 2023
                        AND c.record_status=1
""",
            "result": """[(627)]""",
            "answer": """627 SHGs formed between Jan to March 2023"""
        },
        {
            "input": "What is the count of SHGs formed in Saharsa district in 2022?",
            "sql_cmd": """SELECT
                COUNT(*) AS shg_count
                FROM
                m_cbo c
                INNER JOIN
                m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                INNER JOIN
                m_district d ON c.district_id = d.district_id
                WHERE
                upper(t.type_short_name) = 'SHG'
                AND upper(d.district_name) = 'SAHARSA'
                AND EXTRACT(YEAR FROM c.formation_date) = 2022
                AND c.record_status=1""",
            "result": """[(222)]""",
            "answer": """total 222 SHGs formed in Saharsa district in 2022""",
        },
        {
            "input": "total count of shg",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS shg_count \
                            FROM m_cbo c \
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id \
                            WHERE upper(t.type_short_name) = 'SHG' \
                            AND c.record_status=1""",
            "result": """[(1075033)]""",
            "answer": """There are total 1075033 SHG """,
        },
        {
            "input": "What is the total count of shg?",
            "sql_cmd": """SELECT COUNT(c.cbo_id) AS shg_count \
                            FROM m_cbo c \
                            INNER JOIN m_cbo_type t ON c.cbo_type_id = t.cbo_type_id \
                            WHERE upper(t.type_short_name) = 'SHG' \
                            AND c.record_status=1""",
            "result": """[(1075033)]""",
            "answer": """There are total 1075033 SHG """,
        },
        {
             "input": "How many SHGs in Patna district formed between Jan to March 2023?",
            "sql_cmd": """
                                SELECT
                                    COUNT(*) AS shg_count
                                FROM
                                    m_cbo c
                                INNER JOIN
                                    m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                                INNER JOIN
                                    m_district d ON c.district_id = d.district_id
                                WHERE
                                    upper(t.type_short_name) = 'SHG'
                                    AND upper(d.district_name) = 'PATNA'
                                    AND EXTRACT(MONTH FROM c.formation_date) BETWEEN 1 AND 3
                                    AND EXTRACT(YEAR FROM c.formation_date) = 2023
                                    AND c.record_status = 1
                            """,
            "result": """[(631)]""",
            "answer": """There are total 631 SHG formed in Patna district between Jan to March 2023 """,
        },
        {
            "input": "Number of cbo per block per district",
            "sql_cmd": """
                                SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
                                FROM m_cbo c
                                INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
                                INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
                                WHERE c.record_status = 1
                                GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
                                ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
                            """,
            "result": """[(ARARIA	Araria	4560
                                    ARARIA	Bhargama	3278
                                    ARARIA	Forbesganj	3726
                                    ARARIA	Jokihat	3147
                                    ARARIA	Kursakatta	2205)]""",
            "answer": """ARARIA	Araria	4560
                            ARARIA	Bhargama	3278
                            ARARIA	Forbesganj	3726
                            ARARIA	Jokihat	3147
                            ARARIA	Kursakatta	2205""",
        },
        {
             "input": "What is the distribution of Community Based Organizations (CBOs) by their types, and how many CBOs are there for each type",
            "sql_cmd": """SELECT t.TYPE_SHORT_NAME, COUNT(c.CBO_ID) AS cbo_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                            WHERE c.record_status = 1
                            GROUP BY t.TYPE_SHORT_NAME
                            ORDER BY cbo_count DESC""",
            "result": """[(SHG	1073354
                                VO	75448
                                PG	5998
                                CLF	1658
                                TLC	29
                                PC	18)]""",
            "answer": """there are SHG	1073354
                                VO	75448
                                PG	5998
                                CLF	1658
                                TLC	29
                                PC	18""",
        },
        {
            "input": "What is the most common CBO type in district Vaishali?",
            "sql_cmd": """SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
                        FROM M_CBO C
                        INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
                        WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME)= 'VAISHALI')
                        AND C.RECORD_STATUS = 1
                        GROUP BY TYPE_DESCRIPTION
                        ORDER BY CBO_COUNT DESC
""",
            "result": """[(Self Helped Group	37395
                            village Organization	2653
                            Producer Group	241
                            Cluster Level Federa	60
                            Producer Company	3)]""",
            "answer": """There are Self Helped Group	37395
                            village Organization	2653
                            Producer Group	241
                            Cluster Level Federa	60
                            Producer Company	3 in Vaishali"""
        },
        {
            "input": "give me count of panchayat wise shg from patna district?",
            "sql_cmd": """SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
                        WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC""",
            "result": """[(1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025)]""",
            "answer": """1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025""",
        },
        {
            "input": "give me count of panchayat wise shg from patna district?",
            "sql_cmd": """SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.block_id = p.block_id
                        WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC""",
            "result": """[(1456)]""",
            "answer": """There are 1456 shg in lakhani bigha panchayat""",
        },
        {
            "input": "give me count of panchayat wise shg from patna district?",
            "sql_cmd": """SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
                        WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC""",
            "result": """[(1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025)]""",
            "answer": """1. BARA - 4592 2. IBRAHIMPUR - 4190 3. BARAH - 4150 4. DARIYAPUR - 3959 5. GHOSWARI - 3025""",
        },
        {
            "input": "how many shg in lakhani bigha panchayat?",
            "sql_cmd": """SELECT
    COUNT(c.CBO_ID) AS shg_count
FROM
    m_cbo c
INNER JOIN
    m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
INNER JOIN
    m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
INNER JOIN
    m_block b ON c.BLOCK_ID = b.BLOCK_ID
INNER JOIN
    m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
WHERE
    upper(t.TYPE_SHORT_NAME) = 'SHG'
    AND upper(p.PANCHAYAT_NAME) = 'LAKHANI BIGHA'
    AND c.record_status = 1""",
            "result": """[(1456)]""",
            "answer": """There are 1456 shg in lakhani bigha panchayat"""
        },
        {
            "input": "give me toatal members between 2020 and 2021",
            "sql_cmd": """SELECT 
                            COUNT(DISTINCT m.member_id) AS total_members
                            FROM
                            m_cbo_member m
                            INNER JOIN
                            mp_cbo_member t on m.member_id=t.member_id
                            INNER JOIN
                            m_cbo c ON t.cbo_id = c.cbo_id
                            WHERE
                            EXTRACT(YEAR FROM m.date_of_joining) BETWEEN 2020 AND 2021
                            AND c.record_status=1""",
            "result": """[(1652157)]""",
            "answer": """There are total 1652157 members""",
        },
        {
            "input": "total cadre in shg",
            "sql_cmd": """SELECT
    COUNT(DISTINCT m.MEMBER_ID) AS cadre_count
FROM
    m_cbo_member m
INNER JOIN
   mp_cbo_member t ON m.member_id=t.member_id
INNER JOIN 
  m_designation l ON l.designation_id=t.designation_id
INNER JOIN
    m_cbo c ON t.CBO_ID = c.CBO_ID
INNER JOIN
    m_cbo_type k ON c.CBO_TYPE_ID = k.CBO_TYPE_ID
WHERE
l.member_group_id=3
AND
l.designation_id!=31
  AND  upper(k.TYPE_SHORT_NAME) = 'SHG'
    
    AND c.record_status = 1
    AND t.record_status=1
    AND m.record_status=1""",
            "result": """[(89603)]""",
            "answer": """There are total 89603 in SHG """
        }]
