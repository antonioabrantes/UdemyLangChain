# no JupiterLab: cd Lin_AI_Agents/chap2
# python main_chp2.py

#No power Shell do Jupiter
#Get-Content "..\.env" | ForEach-Object {
#    if ($_ -match "^\s*([A-Z_]+)\s*=\s*(.+)\s*$") {
#        $name = $matches[1]
#        $value = $matches[2]
#        # Define a variável de ambiente apenas para a sessão atual
#        [System.Environment]::SetEnvironmentVariable($name, $value, "Process")
#    }
#}
#echo $env:OPENAI_API_KEY
#$headers = @{
#    "Content-Type" = "application/json"
#    "Authorization" = "Bearer $env:OPENAI_API_KEY"
#}
#$body = @{
#    model = "gpt-4o-mini"
#    input = "Write a one-sentence bedtime story about a unicorn."
#} | ConvertTo-Json
#$response=Invoke-RestMethod -Uri "https://api.openai.com/v1/responses" -Method Post -Headers $headers -Body $body
#$output = $response.output[0].content
#$output.text

from openai import OpenAI
from dotenv import load_dotenv
import os

#load_dotenv()
load_dotenv(dotenv_path='../.env')
openai_api_key = os.getenv("OPENAI_API_KEY")

#client = OpenAI()
client = OpenAI(api_key = openai_api_key)

def summarize_text(text: str) -> str:
    prompt = f"""
        You are a helpful assistant that summarizes text into a tweet. 
        Please summarize the following:
        <text>
        {text}
        </text>
    """

    #response = client.responses.create(
    #    model="gpt-4o",
    #    input = prompt
    #)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content": prompt}])

    #return response.output_text
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    usr_input = input("What text do you want to summarize? ")
    summary = summarize_text(usr_input)
    print("🔍 Summary:\n", summary)
