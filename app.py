import tkinter as tk
from tkinter import ttk, filedialog
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

def read_html_file(file_name):
    with open(file_name, 'r') as file: html_content=file.read()
    soup=BeautifulSoup(html_content, 'html.parser') 
    print(soup.prettify())
    
    variableNames= soup.find_all('div',{'class':'BasicCellContentWrapper-sc-90zwts-0 dfaLxd'})

    varName=[]
    for name in variableNames:print( name.get_text())
    for name in variableNames: varName.append(name.get_text())

    num_columns=3
    words_per_columns=len(varName) // num_columns

    varNameData= [(varName[i], varName[i+1] if i + 1 <len(varName) else '') for i in range(0, len(varName), num_columns)]

##for i in range(0, len(varName), num_columns):
##    print('{:15}{}'.format(varName[i], varName[i+1] if i + 1 <len(varName) else ''))

    namedf=pd.DataFrame(varNameData, columns=['Field Name', 'Variable Name'])

    nameddf1=namedf[['Field Name']]

    print(nameddf1)

###################################################################################################
## Grab Form names (dd and dt)
    formNames= soup.find_all('dt')
    formName=[]
    for form in formNames:print(form.get_text())
    for form in formNames: formName.append(form.get_text())

    num_columns=2
    words_per_columns=len(formName) // num_columns

    formNameData= [(formName[i], formName[i+1] if i + 1 <len(formName) else '') for i in range(0, len(formName), num_columns)]



    formdf=pd.DataFrame(formNameData, columns=['Form', 'Form_Name'])

    formddf1=formdf[['Form']]

    print(formddf1)

###################################################################################################
## Grab Event names (dd and dt)
    eventNames= soup.find_all('dd')
    eventName=[]
    for event in eventNames:print(event.get_text())
    for event in eventNames: eventName.append(event.get_text())


    num_columns=2
    words_per_columns=len(formName) // num_columns

    eventNameData= [(eventName[i], eventName[i+1] if i + 1 <len(eventName) else '') for i in range(0, len(eventName), num_columns)]



    eventdf=pd.DataFrame(eventNameData, columns=['Event', 'Classification'])

    print(eventdf)


#################################################################################################

    merged_df=pd.merge(pd.merge(formddf1, eventdf, left_index=True, right_index=True), nameddf1, left_index=True, right_index=True)
    print(merged_df)

    
    table_data=merged_df.values.tolist()
    headers=merged_df.columns.tolist()

    table_str=tabulate(table_data, headers=headers, tablefmt='html')
    print(table_str)

    return [table_str]

def sort_data(data, column_index):
    sorted_data=sorted(data, key=lambda x: x[column_index])
    return sorted_data

def browse_file():
    file_path=filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:data=read_html_file(file_path)
   
    sort_data(data,0)
    load_data_into_treeview(sort_data)

def load_data_into_treeview(data): 
    for i in tree.get_children():
        tree.delete(i)

    for row in data: tree.insert("", 'end', values=row)


root=tk.Tk()
root.title("SDV Plan Sorter")


browse_button=tk.Button(root, text="HTML File", command=browse_file)
browse_button.pack(pady=10)

tree =ttk.Treeview(root)
tree['columns']= tuple(range(3))


tree.pack(expand=True, fill=tk.BOTH)

root.mainloop()

    
