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
#import prompted
import psycopg2


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Jeevika_Traces"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__1faaa817b79d42ab9a043148b7094ea9"  # Update to your API key

app = Flask(__name__)
CORS(app)

#postgres_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

#postgres_connection = psycopg2.connect(database='jeevika_data_warehouse', user='postgres', password='1234', host='10.0.0.19', port='5432')

# Example usage:
db_user = 'postgres'
db_password = '1234'
db_host = '10.0.0.19'
db_port = '5432'
db_name = 'jeevika_data_warehouse'


try:
        # Establish connection to the PostgreSQL database
    connection = psycopg2.connect(
            database='jeevika_data_warehouse',
            user='postgres',
            password='1234',
            host='10.0.0.19',
            port='5432'
        )
    print("Successfully connected to the PostgreSQL database")
        
except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL database:", error)


db = SQLDatabase.from_uri(f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",include_tables=["m_cbo","m_cbo_type","m_cbo_member","m_cbo_shg_member","t_cbo_appl_mapping","t_cbo_loan_register","t_acc_voucher","t_cbo_appl_mapping","m_farmer", "m_farmer_crop","m_farmer_crop_technology", "m_farmer_croptype", "m_farmer_land",
"m_farmer_pest_management", "mp_cbo_member","m_farmer_seed", "m_farmer_soil_management","t_mp_farmer_transaction_pest", "t_mp_farmer_transaction_soil","t_mp_trasaction_croptechnology","m_block",
"m_district","m_designation","m_village","m_panchayat"])

#print(db.get_usable_table_names())

print(db.get_context())

llm = ChatGoogleGenerativeAI(model="gemini-pro",convert_system_message_to_human=True,google_api_key='AIzaSyCoPL_q2SIKtVEbn6MlvbSnf-MrFnfr9aQ', temperature=0)

#google_api_key='AIzaSyCoPL_q2SIKtVEbn6MlvbSnf-MrFnfr9aQ'
#api_key="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"
# llm = ChatVertexAI(
#     model_name="codechat-bison", max_output_tokens=1000, temperature=0.5
# )

#llm = ChatGooglePalm(google_api_key='AIzaSyCoPL_q2SIKtVEbn6MlvbSnf-MrFnfr9aQ', temperature=0)


example_prompt = PromptTemplate(
input_variables=["input", "sql_cmd", "result", "answer",],
template="\nQuestion: {input}\nSQLQuery: {sql_cmd}\nSQLResult: {result}\nAnswer: {answer}",
)

# examples=prompted.main()
# print(examples)

embeddings = HuggingFaceEmbeddings()

to_vectorize = [" ".join(example.values()) for example in examples]
print('t1')

vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=examples)
print('t2')
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=1,
)



    
   
#print(connection.version)
_postgres_prompt = """You are a postgres SQL expert. Given an input question, first create a syntactically correct postgres SQL query to run,.....and keep in mind its very very important that while generating sql query donot put ;(semicolon) in the end of query or any special character or brackets at begining or end only give sql query.. then look at the results of the query and return the answer to the input question.
Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the WHERE LIMIT<=1 clause as per Postgres SQL. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.Use join and other oracle sql advance query to get the best query according to user query.
Pay attention to use CURRENT_DATE function to get the current date, if the question involves "today".
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
What is the total count of SHG in Patna in 2023?....then query should be...SELECT COUNT(c.CBO_ID) AS shg_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID  
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'SHG' 
                            AND upper(d.DISTRICT_NAME) = 'PATNA' AND EXTRACT(YEAR FROM c.formation_date) = 2023
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
                       where upper(t.type_short_name)= 'SHG'
                        AND upper(d.district_name) = 'NA'
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
                       where upper(t.type_short_name) = 'SHG'
                        AND upper(d.district_name)= 'PATNA'
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
                        Also the 'ROWNUM' condition is applied directly with query , \
                        This is just one example to show you that this kind of mistake should not be done.

                        The right query is:-...


    SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
    FROM m_cbo c
    INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
    INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
    WHERE c.record_status = 1
    GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
    ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
...

For example:-

when i ask....What is the total amount of savings for all SHGs in district Bhojpur?

then the query generated is this \
SELECT SUM(GENERAL_SAVING_AMOUNT + HRF_SAVING_AMOUNT + OTHER_SAVING_1 + OTHER_SAVING_2 + OTHER_SAVING_3) AS total_savings
FROM M_CBO
WHERE DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'BHOJPUR')
AND CBO_TYPE_ID = (SELECT CBO_TYPE_ID FROM M_CBO_TYPE WHERE upper(TYPE_SHORT_NAME) = 'SHG')
AND RECORD_STATUS = 1
WHERE ROWNUM <= 5...which is wrong the right query is.. \

SELECT SUM(GENERAL_SAVING_AMOUNT + HRF_SAVING_AMOUNT + OTHER_SAVING_1 + OTHER_SAVING_2 + OTHER_SAVING_3) AS total_savings
FROM M_CBO
WHERE DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'BHOJPUR')
AND CBO_TYPE_ID = (SELECT CBO_TYPE_ID FROM M_CBO_TYPE WHERE upper(TYPE_SHORT_NAME) = 'SHG')
AND RECORD_STATUS = 1...you can clearly see i have not used WHERE ROWNUM <= 5 which is not required..\



While generating query if the question is to give information for last 2 months or last 3 months or last months,then use (CURRENT_DATE - INTERVAL '' MONTH) to extract the last months information \

Never use ROWNUM with query......

For Example:- 
when asked What is the most common CBO type in district Vaishali?

then query generated is....SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
FROM M_CBO C
INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'VAISHALI')
AND C.RECORD_STATUS = 1
GROUP BY TYPE_DESCRIPTION
ORDER BY CBO_COUNT DESC
WHERE ROWNUM <= 5...which is wrong you can clearly see that ROWNUM has been used directly with query and also ROWNUM is not required here \

The right query is...SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
                        FROM M_CBO C
                        INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
                        WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'VAISHALI')
                        AND C.RECORD_STATUS = 1
                        GROUP BY TYPE_DESCRIPTION
                        ORDER BY CBO_COUNT DESC

fOR eXAMPLE:-
User Question:-give me count of panchayat wise shg from patna district?
The Query you generated is:-SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.PANCHAYAT_ID = p.PANCHAYAT_ID
                        WHERE upper(t.TYPE_SHORT_NAME) = 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC
                        LIMIT 5...here you can clearly see that in (INNER JOIN m_panchayat p ON c.PANCHAYAT_ID = p.PANCHAYAT_ID) there should not be join between m_panchayat and m_cbo table on panchayat_id as m_cbo doesnot contains panchayat_id \

The right Query is:-   SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
FROM m_cbo c
INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
AND upper(d.DISTRICT_NAME) = 'PATNA'
AND c.record_status = 1
GROUP BY p.PANCHAYAT_NAME
ORDER BY shg_count DESC...here you can clearly see as panchayat_id was not present in m_cbo so i searched which columns are common in m_cbo and m_panchayat and founD there was district_id and block_id but i made join on block_id like this (INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID) \

For last 3 months
CURRENT_DATE - INTERVAL '3' MONTH
for last 2 months
CURRENT_DATE - INTERVAL '2' MONTH

for example:
if the question is "total count of cbo formed in sheohar district in last 3 months?" \

the query should be

SELECT COUNT(c.CBO_ID) AS cbo_count
FROM m_cbo c
INNER JOIN m_district d ON c.district_id = d.district_id
WHERE upper(d.district_name) = 'SHEOHAR'
AND c.formation_date >= CURRENT_DATE - INTERVAL '3 MONTH'
AND c.record_status = 1........you can clearly see that it is using CURRENT_DATE - INTERVAL '3' MONTH to extract the last 3 months information..you have to use this method whenever asked about last months question \

and so on \

Some more examples:-

question:-What is the count of all members across SHGs, VOs and CLFs in district Patna?", \

sql query:- SELECT
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'SHG') THEN 1 ELSE 0 END) AS shg_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'VO') THEN 1 ELSE 0 END) AS vo_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'CLF') THEN 1 ELSE 0 END) AS clf_count
FROM m_cbo c
WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'PATNA')
AND c.record_status = 1


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
    prefix=_postgres_prompt+"and keep in mind its very very important that while generating sql query donot put ;(semicolon) in the end of query or any special character or brackets at begining or end only give sql query....... Donot get confused in code and id both are same for example if there is BLOCK_CODE or BLOCK_ID both are same similarly if there is DISTRICT_CODE or DISTRICT_ID both are same ,\
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
                    "mp_cbo_member",
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


# query = full_chain.invoke(
#         {"question": "how many cbo in patna district?" }) 
# print(db.run(query))


@app.route('/response', methods=['POST'])
def api():
    try:
        data = request.get_json()
        question = data.get('question', '')

        try:
            query = full_chain.invoke(
            {"question": question })
            llm2= GoogleGenerativeAI(model="gemini-pro",google_api_key='AIzaSyBZswmKbZf8YzE_41upIXNNwwIh2nkd8v0', temperature=0)

        
            print(query)
        except Exception as e:
             print(e)

        print("-"*20)
        print()
        print()


        try:
            mid_query=llm2(f"""
As an expert in Postgres SQL, your task is to carefully analyze a user's question and the given database schema,....{db.get_context()}... including table names, column names, and their functionality. 
Your role is to write a SQL query that efficiently and accurately retrieves the desired information from the database. However, 
due to the complexity of the database structure or possible misunderstandings of the user's question, 
the initial query which is this... {query}.. may be incorrect. Your responsibility is to identify the important keys present in the schema, check if the generated SQL query can provide the correct answer, 
and ensure that any joins or operations are performed correctly.Here is more informstion about tables and the columns present inside.... \

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
 
While calculating member or if the question contains find or count member then donot join m_cbo and m_cbo_member directly as both does not contain any common column...m_cbo contains cbo_id whereas m_cbo_member contains member_id \
in that case you must use mp_cbo_member which is a mapping table and contains both cbo_id and member_id... \

For example if the question is:-
give me toatal members between 2020 and 2021

then correct query is:-
SELECT 
                            COUNT(DISTINCT m.member_id) AS total_members
                            FROM
                            m_cbo_member m
                            INNER JOIN
                            mp_cbo_member t on m.member_id=t.member_id
                            INNER JOIN
                            m_cbo c ON t.cbo_id = c.cbo_id
                            WHERE
                            EXTRACT(YEAR FROM m.date_of_joining) BETWEEN 2020 AND 2021
                            AND c.record_status=1

        
        Look at the generated sql query which is this {query} and carefully go through it and see in the above tables and math whether the join has been coorectly performed on right columns.
        
        For Example:-

        While generating query you have to take in consideration that only those values are considered whose record_status is 1,this record_status column is present in m_cbo table..so you have to always use where c.record_staus=1 in the query where c is alias name of m_cbo table \
For example if question is like 
What is the total count of SHG in Patna in 2023?....then query should be...SELECT COUNT(c.CBO_ID) AS shg_count
                            FROM m_cbo c
                            INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID  
                            INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                            WHERE upper(t.TYPE_SHORT_NAME) = 'SHG' 
                            AND upper(d.DISTRICT_NAME) = 'PATNA' AND EXTRACT(YEAR FROM c.formation_date) = 2023
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
                       where upper(t.type_short_name)= 'SHG'
                        AND upper(d.district_name) = 'NA'
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
                       where upper(t.type_short_name) = 'SHG'
                        AND upper(d.district_name)= 'PATNA'
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
                        Also the 'ROWNUM' condition is applied directly with query , \
                        This is just one example to show you that this kind of mistake should not be done.

                        The right query is:-...


    SELECT d.DISTRICT_NAME, b.BLOCK_NAME, COUNT(c.CBO_ID) AS cbos
    FROM m_cbo c
    INNER JOIN m_block b ON b.BLOCK_ID = c.BLOCK_ID
    INNER JOIN m_district d ON d.DISTRICT_ID = b.DISTRICT_ID
    WHERE c.record_status = 1
    GROUP BY d.DISTRICT_NAME, b.BLOCK_NAME
    ORDER BY d.DISTRICT_NAME, b.BLOCK_NAME
...

For example:-

when i ask....What is the total amount of savings for all SHGs in district Bhojpur?

then the query generated is this \
SELECT SUM(GENERAL_SAVING_AMOUNT + HRF_SAVING_AMOUNT + OTHER_SAVING_1 + OTHER_SAVING_2 + OTHER_SAVING_3) AS total_savings
FROM M_CBO
WHERE DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'BHOJPUR')
AND CBO_TYPE_ID = (SELECT CBO_TYPE_ID FROM M_CBO_TYPE WHERE upper(TYPE_SHORT_NAME) = 'SHG')
AND RECORD_STATUS = 1
WHERE ROWNUM <= 5...which is wrong the right query is.. \

SELECT SUM(GENERAL_SAVING_AMOUNT + HRF_SAVING_AMOUNT + OTHER_SAVING_1 + OTHER_SAVING_2 + OTHER_SAVING_3) AS total_savings
FROM M_CBO
WHERE DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'BHOJPUR')
AND CBO_TYPE_ID = (SELECT CBO_TYPE_ID FROM M_CBO_TYPE WHERE upper(TYPE_SHORT_NAME) = 'SHG')
AND RECORD_STATUS = 1...you can clearly see i have not used WHERE ROWNUM <= 5 which is not required..\



While generating query if the question is to give information for last 2 months or last 3 months or last months,then use (CURRENT_DATE - INTERVAL '' MONTH) to extract the last months information \

Never use ROWNUM with query...... \

For Example:- 
when asked What is the most common CBO type in district Vaishali?

then query generated is....SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
FROM M_CBO C
INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'VAISHALI')
AND C.RECORD_STATUS = 1
GROUP BY TYPE_DESCRIPTION
ORDER BY CBO_COUNT DESC
WHERE ROWNUM <= 5...which is wrong you can clearly see that ROWNUM has been used directly with query and also ROWNUM is not required here \

The right query is...SELECT TYPE_DESCRIPTION, COUNT(CBO_ID) AS CBO_COUNT
                        FROM M_CBO C
                        INNER JOIN M_CBO_TYPE T ON C.CBO_TYPE_ID = T.CBO_TYPE_ID
                        WHERE C.DISTRICT_ID = (SELECT DISTRICT_ID FROM M_DISTRICT WHERE upper(DISTRICT_NAME) = 'VAISHALI')
                        AND C.RECORD_STATUS = 1
                        GROUP BY TYPE_DESCRIPTION
                        ORDER BY CBO_COUNT DESC

fOR eXAMPLE:-
User Question:-give me count of panchayat wise shg from patna district?
The Query you generated is:-SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
                        FROM m_cbo c
                        INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
                        INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
                        INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
                        INNER JOIN m_panchayat p ON c.PANCHAYAT_ID = p.PANCHAYAT_ID
                        WHERE upper(t.TYPE_SHORT_NAME) = 'SHG'
                        AND upper(d.DISTRICT_NAME) = 'PATNA'
                        AND c.record_status = 1
                        GROUP BY p.PANCHAYAT_NAME
                        ORDER BY shg_count DESC
                        LIMIT 5...here you can clearly see that in (INNER JOIN m_panchayat p ON c.PANCHAYAT_ID = p.PANCHAYAT_ID) there should not be join between m_panchayat and m_cbo table on panchayat_id as m_cbo doesnot contains panchayat_id \

The right Query is:-   SELECT p.PANCHAYAT_NAME, COUNT(c.CBO_ID) AS shg_count
FROM m_cbo c
INNER JOIN m_cbo_type t ON c.CBO_TYPE_ID = t.CBO_TYPE_ID
INNER JOIN m_district d ON c.DISTRICT_ID = d.DISTRICT_ID
INNER JOIN m_block b ON c.BLOCK_ID = b.BLOCK_ID
INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID
WHERE upper(t.TYPE_SHORT_NAME)= 'SHG'
AND upper(d.DISTRICT_NAME) = 'PATNA'
AND c.record_status = 1
GROUP BY p.PANCHAYAT_NAME
ORDER BY shg_count DESC...here you can clearly see as panchayat_id was not present in m_cbo so i searched which columns are common in m_cbo and m_panchayat and foun there was district_id and block_id but i made join on block_id like this (INNER JOIN m_panchayat p ON c.BLOCK_ID = p.BLOCK_ID) \

For last 3 months
CURRENT_DATE - INTERVAL '3 MONTH'
for last 2 months
CURRENT_DATE - INTERVAL '2 MONTH'

for example:
if the question is "total count of cbo formed in sheohar district in last 3 months?" \

the query should be

SELECT COUNT(c.CBO_ID) AS cbo_count
FROM m_cbo c
INNER JOIN m_district d ON c.district_id = d.district_id
WHERE upper(d.district_name) = 'SHEOHAR'
AND c.formation_date >= CURRENT_DATE - INTERVAL '3 MONTH'
AND c.record_status = 1........you can clearly see that it is using CURRENT_DATE - INTERVAL '3 MONTH' to extract the last 3 months information..you have to use this method whenever asked about last months question \

and so on \

Some more examples:-

question:-What is the count of all members across SHGs, VOs and CLFs in district Patna?", \

sql query:- SELECT
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'SHG') THEN 1 ELSE 0 END) AS shg_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'VO') THEN 1 ELSE 0 END) AS vo_count,
    SUM(CASE WHEN cbo_type_id = (SELECT cbo_type_id FROM m_cbo_type WHERE type_short_name = 'CLF') THEN 1 ELSE 0 END) AS clf_count
FROM m_cbo c
WHERE district_id = (SELECT district_id FROM m_district WHERE upper(district_name) = 'PATNA')
AND c.record_status = 1


If you are confident that the generated SQL query is correct, please return the same query as it is...only return the query no statement or anything. 
If there are mistakes or if joins or other operations are not performed correctly, make the necessary changes and return the accurate SQL query.
 Pay particular attention to ensuring that joins are performed on relevant columns present in the respective tables. 
Your optimized response should include the corrected SQL query, if necessary, to retrieve the desired information from the database.""")


        
            print(mid_query)
            print("-"*20)
            print()
            print()

        except Exception as e:
             print(e)
        try:
            final_query=llm2(f"This is a postgres sql query {mid_query} which is going to be executed but if the query contains semicolon(;),WHERE ROWNUM clause in the end or any special character at begining or end except query then it will not run ...your task is to return the same query by removing semicolon(;),WHERE ROWNUM clause  or any special character in the begining or end if it contains..if it does not contain then its good just return the query as it is.")

        
            print(final_query)
        except Exception as e:
             print(e)

        print(db.run(final_query))
        
        response = llm2(f"""this is user question {question} and this is the answer {db.run(final_query)}....combine both to give a natural language answer...this is very important to include only this value {db.run(final_query)} in your answer \ 
        .....answer in pointwise....your final answer must include the values of {db.run(final_query)} \ 
        Remember that vo means village organisation,shg means self help group,cbo means community based organisation and clf means cluster level federation  \
                    Pay attention to not add anything from your side in answer.. just give simple natural language answer including this value {db.run(final_query)}. 
                
                if the answer is like this  [('PURBI CHAMPARAN', 3681), ('MUZAFFARPUR', 3659), ('SAMASTIPUR', 3404), ('GAYA', 3383), ('MADHUBANI', 3382), ('DARBHANGA', 3080), ('PATNA', 2726), ('SITAMARHI', 2706), ('PASHCHIM CHAMPARAN', 2668), ('VAISHALI', 2653), ('PURNIA', 2591), ('SARAN', 2363), ('KATIHAR', 2328), ('ARARIA', 2264), ('NALANDA', 2259), ('SIWAN', 2211), ('SUPAUL', 2122), ('BEGUSARAI', 2016), ('MADHEPURA', 1986), ('BHAGALPUR', 1973), ('AURANGABAD', 1838), ('GOPALGANJ', 1783), ('BANKA', 1743), ('ROHTAS', 1706), ('NAWADA', 1591), ('SAHARSA', 1565), ('BHOJPUR', 1537), ('KISHANGANJ', 1434), ('KHAGARIA', 1421), ('JAMUI', 1288), ('KAIMUR (BHABUA)', 1199), ('BUXAR', 994), ('JEHANABAD', 957), ('MUNGER', 791), ('SHEOHAR', 594), ('LAKHISARAI', 570), ('ARWAL', 570), ('SHEIKHPURA', 443)]...then return as it is...... donot make natural language answer in these kind of answers
                
                For example:-
                
                user question:-district wise count of vo
                
                your response should be:- [('PURBI CHAMPARAN', 3681),
                                            ('MUZAFFARPUR', 3659), 
                                            ('SAMASTIPUR', 3404), 
                                            ('GAYA', 3383), 
                                            ('MADHUBANI', 3382), 
                                            ('DARBHANGA', 3080), 
                                            ('PATNA', 2726), 
                                            ('SITAMARHI', 2706), 
                                            ('PASHCHIM CHAMPARAN', 2668), 
                                            ('VAISHALI', 2653), 
                                            ('PURNIA', 2591), 
                                            ('SARAN', 2363), 
                                            ('KATIHAR', 2328), 
                                            ('ARARIA', 2264), 
                                            ('NALANDA', 2259), 
                                            ('SIWAN', 2211), 
                                            ('SUPAUL', 2122), 
                                            ('BEGUSARAI', 2016), 
                                            ('MADHEPURA', 1986), 
                                            ('BHAGALPUR', 1973), 
                                            ('AURANGABAD', 1838), 
                                            ('GOPALGANJ', 1783), 
                                            ('BANKA', 1743), 
                                            ('ROHTAS', 1706), 
                                            ('NAWADA', 1591), 
                                            ('SAHARSA', 1565), 
                                            ('BHOJPUR', 1537), 
                                            ('KISHANGANJ', 1434), 
                                            ('KHAGARIA', 1421), 
                                            ('JAMUI', 1288), 
                                            ('KAIMUR (BHABUA)', 1199), 
                                            ('BUXAR', 994), 
                                            ('JEHANABAD', 957), 
                                            ('MUNGER', 791), 
                                            ('SHEOHAR', 594), 
                                            ('LAKHISARAI', 570), 
                                            ('ARWAL', 570), 
                                            ('SHEIKHPURA', 443)]""")
        print(response)

        
        print(db.run(final_query))

        print("-"*20)

        cursor = connection.cursor()
       
            
        cursor.execute(final_query)

    
    
    
       
        return jsonify({'response': response})
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
