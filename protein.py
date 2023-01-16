# External libraries
import streamlit as st


# Backend modules
import analysisService

class render_tab3:
    def __init__(self):
        st.info("Analysis of drugs with shared proteins:\n" +
                "Do drugs with shared proteins have common side effects?")
    
    def show_protein_analysis(self):
        """UI for displaying results of shared protein analysis.

        Args:
            selected_sideEffects:
            type: list
            nr_sideEffects:
            type: int
        Returns:
            selected_sideEffects: list of chosen side effects
            type: dataframe
        """
        
        # Analysis
        st.subheader("Procedure of Analysis")
        proc_descr1 = """The basic idea is to check whether <b>(1)</b> at least one side effect occuring with drugs that share a protein,
                        <b>(2)</b> is listed with all drugs that share the protein. The analysis excluded proteins that are targeted only from one drug.<br>
                     """    
        st.markdown(proc_descr1, unsafe_allow_html=True)
        with st.expander("In more detail, the analysis proceeded as follows."):
            proc_descr2 = """
                            <ol>
                            <b>(1) Table 1:</b>
                            <li>For each protein, find the side effects of drugs that share the protein.</li>
                            <li>Calculate the number of occurence of same side effects for each protein.</li>
                            <b>(2) Table 2:</b>
                            <li>Find proteins with their shared drugs.</li>
                            <li>For each protein, calculate the total number of drugs that share the protein.</li>
                            <b>Connect results from (1) and (2):</b>
                            <li>Join the tables from (1) and (2) on the proteins.</li>
                            <li>For each protein, calculate the ratio of side effects to the number of drugs that share the protein.</li>
                            <b>Make general statement with an average:</b>
                            <li>Calculate the average ratio from step 6 over all proteins and side effects.</li>
                            </ol>
                            <br>
                        """
        
            st.markdown(proc_descr2, unsafe_allow_html=True)

        


        with st.expander("Procedure as SQL-Query"):
            query = """
    /* Calculate avg. ratio from side effects common in meds with a shared protein */
    select to_char((avg(full_table.ratio_common_se))*100, 'fm900D00%') as avg_ratio_common_se
    from

    /* Calculate the ratio from side effects common in meds with a shared protein */
    (select gene_sideeffects.gene1 as gene, gene_sideeffects.se as side_effect,
    gene_sideeffects.nr_shared_se as nr_common_se, shared_meds.nr_shared_meds as nr_shared_meds,
    gene_sideeffects.nr_shared_se::float/shared_meds.nr_shared_meds as ratio_common_se,
    to_char((gene_sideeffects.nr_shared_se::float/shared_meds.nr_shared_meds)*100, 'fm900D00%') as per_ratio_common_se

    from
    /* Table 1 with proteins with side effects from shared meds */
    (select mp1.gene as gene1, mm.individual_side_effect as se, count(*) as nr_shared_se
    from dbms.medicine_protein mp1, dbms.medicine_mono mm
    where mp1.stitch = mm.stitch
    group by mp1.gene, mm.individual_side_effect)gene_sideeffects,

    /* Table 2 with proteins with their shared meds */
    (select mp.gene as gene2, count(*) as nr_shared_meds
    from dbms.medicine_protein mp
    group by gene)shared_meds

    /* Join Table 1 with Table 2 on the protein and exclude proteins that are targeted
    only in one medicine */
    where gene_sideeffects.gene1 = shared_meds.gene2
    and shared_meds.nr_shared_meds > 1)full_table
                    """
        
            st.code(query, language="sql")

        st.warning("NOTICE: The execution of this analysis may take up to about 02:30mins, since it is processed (processing of > 1,5mio rows) during runtime instead of accessing a final result.")

        if st.button(label="Execute Analysis"):
            #st.spinner("Execution may require up to 2:30mins...")
            # Runtime analysis execution
            protein_data = analysisService.data4Analysis()
            avg_ratio_se_meds, result_analysis = protein_data.lookup_avg_ratio_se_meds()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display result of analysis
            if result_analysis == "False":
                result_display = "No, drugs with shared proteins do not - on average - have common side effects. On average one side effect of drugs with a shared protein is common only in <b>" + avg_ratio_se_meds + "</b> of all drugs with this shared protein."
                st.subheader("Result of Analysis: No")     
                st.markdown(result_display, unsafe_allow_html=True)
            else:
                result_display = "Yes, drugs with shared proteins do - on average - have common side effects. On average one side effect of drugs with a shared protein is common in <b>" + avg_ratio_se_meds + "</b> of all drugs with this shared protein."
                st.subheader("Result of Analysis: Yes")     
                st.markdown(result_display, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)    
        
        return avg_ratio_se_meds

    
    def show_protein_analysis_details(self):
        """UI for displaying results of shared protein analysis.

        Args:
            selected_sideEffects:
            type: list
            nr_sideEffects:
            type: int
        Returns:
            selected_sideEffects: list of chosen side effects
            type: dataframe
        """
        # Details
        st.subheader("Want to explore data in more detail?")     
        # Data basis table
        with st.expander("Query for data basis"):
            st.write("Notice that this query is limited to 100 rows because the processing of > 1,5mio rows would require to many resources. The target here is to get an feeling for the data and prodecure applied to the analysis.")
            
            query_total = """/* Relevant attributes */
select gene_sideeffects.gene1 as gene, gene_sideeffects.se as side_effect, gene_sideeffects.nr_shared_se as nr_common_se,
shared_meds.nr_shared_meds as nr_shared_meds,
to_char((gene_sideeffects.nr_shared_se::float/shared_meds.nr_shared_meds)*100, 'fm900D00%') as per_ratio_common_se

from
/* (1): Table 1 for analysis */
(select mp1.gene as gene1, mm.individual_side_effect as se, count(*) as nr_shared_se
 from dbms.medicine_protein mp1, dbms.medicine_mono mm
 where mp1.stitch = mm.stitch
 group by mp1.gene, mm.individual_side_effect)gene_sideeffects,
/* (2): Table 2 for analysis */
(select mp.gene as gene2, count(*) as nr_shared_meds
from dbms.medicine_protein mp
group by gene)shared_meds

/* Join tables on proteins and exclude proteins that are only targeted by one medicine */
where gene_sideeffects.gene1 = shared_meds.gene2 and shared_meds.nr_shared_meds > 1

/* Limit to 100 rows */
limit 100"""

            st.code(query_total, language="sql")
            
        st.warning("NOTICE: The execution of this query may take up to about 02:30mins, since the query is executed during runtime instead of accessing a final result.")
        if st.button(label="Execute Query"):
            #st.spinner("Execution may require up to 2:30mins...")
            # Runtime analysis execution
            protein_data = analysisService.data4Analysis()
            data_basis = protein_data.lookup_protein_se_meds()
            
            st.markdown("<br><b>Excerp of data basis for the analaysis:</b><br>", unsafe_allow_html=True)
            st.write(data_basis)


        return None


if __name__ == "__main__":
    pass