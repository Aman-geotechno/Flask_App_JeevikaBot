from langchain_community.utilities import SQLDatabase
import streamlit as st
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from operator import itemgetter
from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX
from langchain.prompts.prompt import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate

import cx_Oracle
import os
from sqlalchemy import create_engine
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI,ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from prompted import examples
from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask
from flask_cors import CORS
#from langchain_google_vertexai import ChatVertexAI
from langchain_community.chat_models import ChatGooglePalm

app = Flask(__name__)
CORS(app)


instant_client_dir = r'C:\instantclient-basic-windows.x64-21.12.0.0.0dbru\instantclient_21_12'
os.environ["PATH"] = f"{instant_client_dir};{os.environ['PATH']}"

db_user = "readonlyu"
db_password = "rou"
db_host = "10.0.4.4"
db_port = "1521"  
db_service_name = "CBO"
db_name="BRLPS_CBO_MIS"

oracle_connection_string = f"{db_user}/{db_password}@{db_host}:{db_port}/{db_service_name}"

try:
    connection = cx_Oracle.connect(oracle_connection_string)

    print(connection.version)
except:
    print("Database not connected.Check your connection.")





engine = create_engine(f"oracle+cx_oracle://{db_user}:{db_password}@{db_host}:{db_port}/{db_service_name}",echo=True)
db = SQLDatabase.from_uri(f"oracle+cx_oracle://{db_user}:{db_password}@{db_host}:{db_port}/{db_service_name}",schema="BRLPS_CBO_MIS",include_tables=["m_cbo","m_cbo_type","m_cbo_member","m_cbo_shg_member","t_cbo_appl_mapping","t_cbo_loan_register","t_acc_voucher","t_cbo_appl_mapping","m_farmer", "m_farmer_crop","m_farmer_crop_technology", "m_farmer_croptype", "m_farmer_land",
"m_farmer_pest_management", "m_farmer_seed", "m_farmer_soil_management","t_mp_farmer_transaction_pest", "t_mp_farmer_transaction_soil","t_mp_trasaction_croptechnology","m_block",
"m_district","m_designation","m_village","m_panchayat"])


llm = ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True,google_api_key='AIzaSyCoPL_q2SIKtVEbn6MlvbSnf-MrFnfr9aQ', temperature=0)
#api_key="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"
# llm = ChatVertexAI(
#     model_name="codechat-bison", max_output_tokens=1000, temperature=0.5
# )

#llm = ChatGooglePalm(google_api_key='AIzaSyCoPL_q2SIKtVEbn6MlvbSnf-MrFnfr9aQ', temperature=0)


example_prompt = PromptTemplate(
input_variables=["input", "sql_cmd", "result", "answer",],
template="\nQuestion: {input}\nSQLQuery: {sql_cmd}\nSQLResult: {result}\nAnswer: {answer}",
)


embeddings = HuggingFaceEmbeddings()

to_vectorize = [" ".join(example.values()) for example in examples]
print('t1')

vectorstore = FAISS.from_texts(to_vectorize, embeddings, metadatas=examples)
print('t2')
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=1,
)



    
   
print(connection.version)
_oracle_prompt = """You are an Oracle SQL expert. Given an input question, first create a syntactically correct Oracle SQL query to run,.....and keep in mind its very very important that while generating sql query donot put ;(semicolon) in the end of query or any special character or brackets at begining or end only give sql query.. then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the WHERE ROWNUM <= 1 clause as per Oracle SQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.Use join and other oracle sql advance query to get the best query according to user query.
Pay attention to use SYSDATE function to get the current date, if the question involves "today".Also pay attention to use only last two digit of year for example if year is 2023 then use 23,if year is 2012 then use 12.
Pay attention to write district name in capital letter while generating sql query..for example DISTRICT_NAME='DARBHANGA'
Detail information about table and its columns are as follows:-
       
       The table M_CBO is a master table storing information about Community Based Organizations (CBOs),vo(Village Organisation),shg(Self Help Group) and clf(Cluster Level Federation) with columns including CBO_ID, CBO_NAME, DISTRICT_ID, BLOCK_ID, VILLAGE_ID, CBO_TYPE_ID, THEME_ID, LATITUDE, LONGITUDE, TOLA_MOHALLA_NAME, MEETING_PERIODICITY, MEETING_DAY, MEETING_DATE, GENERAL_SAVING_AMOUNT, HRF_SAVING_AMOUNT, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, SHARE_RATE, MEETING_START_TIME, STATE_ID, FORMATION_DATE, SCHEME_ID, CBO_NAME_HINDI, OTHER_SAVING_1, OTHER_SAVING_2, OTHER_SAVING_3, MEMBERSHIP_FEE, REGISTRATION_NUMBER, REGISTRATION_DATE, COMPLETE_STATUS, NRLM_CODE, PWD, LOKOS_CODE.\n
        The table M_CBO_TYPE is a master table containing information about different types of Community Based Organizations (CBO types) with columns such as CBO_TYPE_ID, TYPE_SHORT_NAME, TYPE_DESCRIPTION, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, TYPE_SHORT_NAME_HINDI, TYPE_DESCRIPTION_HINDI, PARENT_CBO_TYPE_ID.\n
       The table M_CBO_MEMBER is a master table containing information about individual members of a Community Based Organization (CBO) with columns such as MEMBER_ID, NAME, FATHER_NAME, HUSBAND_NAME, DOB (Date of Birth), GENDER, ADDRESS, EDUCATION, DATE_OF_JOINING, EMAIL_ADDRESS, PHONE_NO, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, RECORD_STATUS, STATE_ID, DISTRICT_ID, BLOCK_ID, VILLAGE_ID, NAME_HINDI, FATHER_NAME_HINDI, HUSBAND_NAME_HINDI, POSTOFFICE, THANA, KYC_TYPE, KYC_NUMBER, EBS_MEMBER_ID, SECC_PIN_NO, STATEID, DISTRICTID, BLOCKID, VILLAGEID, TOILET, AADHAR_NUMBER, AADHER_CARD_SEEDED, NRLM_MEMBER_ID, REF_CODE, AADHAR_STATUS, LOKOS_MEMBER_CODE.\n
       The table M_CBO_SHG_MEMBER is a master table that stores detailed information about individual members associated with a Self Help Group (SHG) within a Community Based Organization (CBO). It includes columns such as MEMBER_ID, CATEGORY, CASTE, RELIGION, TOLA_NAME, CREATED_BY, UPDATED_BY, CREATED_ON, UPDATED_ON, RECORD_STATUS, CBO_ID, ENDORSED_BY_GRAMSABHA, DISTRICTID.\n
       The table T_CBO_APPL_MAPPING is a transactional table responsible for storing information related to transactions involving the mapping of applications to a Community Based Organization (CBO). It includes columns such as APPLICATION_ID, ACC_NUMBER, ACC_OPENING_DATE, ACC_OPENING_STATUS, CBO_ID, CREATED_ON, UPDATED_ON, CREATED_BY, and UPDATED_BY to track transactional details associated with this mapping.\n
       The table T_CBO_LOAN_REGISTER is a transactional table that maintains records of loans registered within a Community Based Organization (CBO). It contains columns such as LOAN_REGISTER_ID, CBO_ID, LOAN_TYPE_ID, LOAN_AMOUNT, LOAN_INSTALLMENTS, LOAN_DATE, RECORD_UPDATED_ON, RECORD_UPDATED_BY, RECORD_CREATED_ON, RECORD_CREATED_BY, LOAN_REASON, INTEREST_AMOUNT, PAID, TILL_DATE, LOAN_FROM_CBO_ID, IMEI_NUMBER, and RECORD_SYNCED_ON.\n
       The table T_ACC_VOUCHER is a transactional table that stores accounting vouchers within the context of a Community Based Organization (CBO). It includes columns such as VOUCHER_ID, VOUCHER_DATE, CBO_ID, DEBIT_ACCOUNT, CREDIT_ACCOUNT, REMARKS, OTHER_NAME, DEBIT_STAKEHOLDER_ID, VOUCHER_TYPE_ID, CREATED_ON, CREATED_BY, CREDIT_STAKEHOLDER_ID, IMEI_NUMBER, RECORD_SYNCED_ON, CHEQUE_NO, and CHEQUE_DATE. \n
       The table M_BLOCK represents information about different blocks. It includes columns such as BLOCK_ID, BLOCK_NAME, DISTRICT_ID, STATE_ID, BLOCK_NAME_HINDI, NRLM_BLOCK_CODE, ADDOPED_BY_SCHEME, PROJECT_CODE, and PROJECT_CODE_TILL_APRIL_2023. \n
       The table M_DISTRICT contains information about different districts. It includes columns such as DISTRICT_ID, DISTRICT_NAME, STATE_ID, DISTRICT_NAME_HINDI, DISTRICT_CENS_2011_ID, and NRLM_DISTRICT_CODE.\n
       The table M_PANCHAYAT contains information about various panchayats. It includes columns such as STATE_ID, DISTRICT_ID, BLOCK_ID, PANCHAYAT_ID, PANCHAYAT_NAME, PANCHAYAT_NAME_HINDI, and NRLM_PANCHAYAT_CODE. \n
       The table M_VILLAGE contains information about various villages. It includes columns such as VILLAGE_ID, VILLAGE_NAME, BLOCK_ID, OTHER_POPULATION, SC_POPULATION, ST_POPULATION, DISTRICT_ID, STATE_ID, PANCHAYAT_ID, VILLAGE_NAME_HINDI, EBC_POPULATION, BC_POPULATION, MD_POPULATION, and NRLM_VILLAGE_CODE. \n
       The table MP_CBO_MEMBER is a mapping table that associates members with a specific Community Based Organization (CBO). It includes columns such as MEMBER_ID, CBO_ID, DESIGNATION_ID, RECORD_STATUS, ID, CREATED_BY, CREATED_ON, UPDATED_BY, UPDATED_ON, and DISTRICTID.\n
        T_BULK_BANK_ACC is a transactional tabe which contains columns APPLICATION_ID BRANCH_ID,ACC_TYPE_ID,APPLICATION_DATE,CREATED_ON,UPDATED_ON,BANK_ID,NO_OF_APPLICATIONS,STATUS,REMARKS,ACCOUNT_HOLDER_TYPE this able is used in conjunction with other tables when question asked about saving account of shg,vo or clf

While generating query you have to take in consideration that only those values are considered whose record_status is 1,this record_status column is present in m_cbo table..so you have to always use where c.record_staus=1 in the query where c is alias name of m_cbo table \
For example if question is like 
What is the total count of SHG?....then query should be...SELECT COUNT(c.CBO_ID) AS shg_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID  
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE t.TYPE_SHORT_NAME = 'SHG' 
                            AND d.DISTRICT_NAME = 'PATNA' AND SUBSTR(c.formation_date, -2) = '23'
                            AND c.record_status=1...you can clearly see c.record_status=1 has been used which is important to get only the information for those values which are live..so this c.record_status=1 will be used almost in all sq query.

While generating sql query donot do any silly mistakes or donot give wrong query...this query will be used for very important person whch is related to their livelihoods \
For example:-

When I asked "how many shg in patna district are there?"
You returned query this..SELECT
                        (*) AS shg_count
                        m_cbo c
                        INNER JOIN
                        m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                        INNER JOIN
                        m_district d ON c.district_id = d.district_id
                        t.type_short_name = 'SHG'
                        AND d.district_name = 'NA'
                        AND c.record_status=1.......which is wrong you can clearly see that you have taken d.district_name='NA'...it should be d.district_name='PATNA' \

                        This is just one example to show you that this kind of mistake should not be done.

                        The right query is:-...

                        SELECT
                        (*) AS shg_count
                        m_cbo c
                        INNER JOIN
                        m_cbo_type t ON c.cbo_type_id = t.cbo_type_id
                        INNER JOIN
                        m_district d ON c.district_id = d.district_id
                        t.type_short_name = 'SHG'
                        AND d.district_name = 'PATNA'
                        AND c.record_status=1

While generating sql it is very important to not put or use semicolon(;) at the end of query \

When I asked "Number of cbo per block per district"
You returned query this..SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
FROM m_cbo c
INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
WHERE c.record_status=1
GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
WHERE ROWNUM <= 5;.......which is wrong you can clearly see that you have used semicolon(;) at the end of query..you should not use semicolon(;) \

                        This is just one example to show you that this kind of mistake should not be done.

                        The right query is:-...

                        SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
FROM m_cbo c
INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
WHERE c.record_status=1
GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
WHERE ROWNUM <= 5

For example
Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

"""
few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_oracle_prompt+"and keep in mind its very very important that while generating sql query donot put ;(semicolon) in the end of query or any special character or brackets at begining or end only give sql query....... Donot get confused in code and id both are same for example if there is BLOCK_CODE or BLOCK_ID both are same similarly if there is DISTRICT_CODE or DISTRICT_ID both are same ,\
same goes for village_id and village_code and panchayat_id and panchayat_code and clf_id and clf_code.\
You cannot perform join on clf_id with village_id or block_id or block_code\
but you can perform join on village_id and village_code ,similar for district_id and district_code and block_id and block_code.\
    ",
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], 
)
query_chain = create_sql_query_chain(llm, db,prompt=few_shot_prompt)

    

  




class Table(BaseModel):
        """Table in SQL database."""

        name: str = Field(description="Name of table in SQL database.")

table_names = "\n".join(db.get_usable_table_names())
system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

    {table_names}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)



system = f"""Return the names of the SQL tables that are relevant to the user question. \
The tables are:

CBO
Farmer"""
category_chain = create_extraction_chain_pydantic(Table, llm, system_message=system)


from typing import List


def get_tables(categories: List[Table]) -> List[str]:
        tables = []
        for category in categories:
            if category.name == "CBO":
                tables.extend(
                [
                    "m_cbo",
                    "m_cbo_type",
                    "m_cbo_member",
                    "m_cbo_shg_member",
                    "t_cbo_appl_mapping",
                    "t_cbo_loan_register",
                    "t_acc_voucher",
                    "t_cbo_appl_mapping",
                    
                    "m_block",
                    "m_district",
                    "m_designation",
                    "m_village",
                    "m_panchayat"
                ]
            )
            elif category.name == "Farmer":
                tables.extend(["m_farmer", "m_farmer_crop","m_farmer_crop_technology", "m_farmer_croptype", "m_farmer_land",
                            "m_farmer_pest_management", "m_farmer_seed", "m_farmer_soil_management","t_mp_farmer_transaction_pest", "t_mp_farmer_transaction_soil","t_mp_trasaction_croptechnology"])
        return tables


table_chain = category_chain | get_tables
table_chain = {"input": itemgetter("question")} | table_chain

full_chain = RunnablePassthrough.assign(table_names_to_use=table_chain) | query_chain


query = full_chain.invoke(
        {"question": "how many cbo in patna district?" }) 



# @app.route('/response', methods=['POST'])
# def api():
#     try:
#         data = request.get_json()
#         question = data.get('question', '')
#         query = full_chain.invoke(
#         {"question": question })
#         llm2= GoogleGenerativeAI(model="gemini-pro",google_api_key='AIzaSyBZswmKbZf8YzE_41upIXNNwwIh2nkd8v0', temperature=0)
    
            
#         final_query=llm2(f"This is a oracle sql query {query} which is going to be executed but if the query contains semicolon in the end or any special character at begining or end except query then it will not run ...your task is to return the same query by removing semicolon(;) or any special character in the begining or end if it contains..if it does not contain then its good just return the query as it is.")
#         print(final_query)
#         response = llm2(f"""this is user question {question} and this is the answer {db.run(final_query)}....combine both to give a natural language answer...this is very important to include only this value {db.run(final_query)} in your answer \ 
#         .....answer in pointwise....your final answer must include the values of {db.run(final_query)} \ 
#         Remember that vo means village organisation,shg means self help group,cbo means community based organisation and clf means cluster level federation \
#                     Pay attention to not add anything from your side in answer.. just give simple natural language answer including this value {db.run(final_query)}. 
                
#                 if the answer has many rows or columns then only give first five answer for example if answer is like this \ 
#                                                             ARARIA	2309
#                                                             JAMUI	1293
#                                                             JEHANABAD	963
#                                                             KAIMUR (BHABUA)	1205
#                                                             MUZAFFARPUR	3717
#                                                             SHEIKHPURA	445
#                                                             AURANGABAD	1847
#                                                             KATIHAR	2365
#                                                             NALANDA	2298
#                                                             SAMASTIPUR	3449
#                                                             SUPAUL	2131
#                                                             GOPALGANJ	1806
#                                                             KISHANGANJ	1443
#                                                             NAWADA	1612
#                                                             PURNIA	2655
#                                                             SITAMARHI	2733
#                                                             BHAGALPUR	2062
#                                                             BHOJPUR	1580
#                                                             DARBHANGA	3170
#                                                             SAHARSA	1568
#                                                             SHEOHAR	605
#                                                             LAKHISARAI	572
#                                                             MUNGER	802
#                                                             SARAN	2374
#                                                             BUXAR	998
#                                                             MADHUBANI	3384
#                                                             PATNA	2725
#                                                             PURBI CHAMPARAN	3721
#                                                             ROHTAS	1751
#                                                             SIWAN	2214
#                                                             BANKA	1761
#                                                             BEGUSARAI	2019
#                                                             KHAGARIA	1484
#                                                             MADHEPURA	2006
#                                                             PASHCHIM CHAMPARAN	2676
#                                                             VAISHALI	2666
#                                                             GAYA	3404
#                                                             ARWAL	579......then your answer should be this... \
#                                                             JAMUI	1293
#                                                             JEHANABAD	963
#                                                             KAIMUR (BHABUA)	1205
#                                                             MUZAFFARPUR	3717
#                                                            SHEIKHPURA	445""")
#         print(response)
#         print(db.run(final_query))

#         print("-"*20)
#         cursor = connection.cursor()
#         cursor.execute(final_query)
    
#     # Fetch the results
#         rows = cursor.fetchall()
    
#     # Print the results
#         for row in rows:
#             print(row)
#         return jsonify({'response': response})
#     except SQLAlchemyError as e:
#         return jsonify({'error': f'Database error: {str(e)}'}), 500
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
