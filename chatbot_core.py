import json
from typing import Dict, List, Optional, Union
from pathlib import Path
from dataclasses import dataclass

@dataclass
class Question:
    text: str
    options: List[str]
    next_steps: Dict[str, Union[str, Dict]]

@dataclass
class Diagnosis:
    category: str
    causes: str
    specialist: str

class ChatbotCore:
    def __init__(self, rules_file: str = "rules.json"):
        self.rules = self._load_rules(rules_file)
        self.current_language = "en"
        self.current_concern = None
        self.chat_history = []
        self.current_question = None
        self.analysis_points = []
        self._initialize_flowcharts()
        
    def _load_rules(self, rules_file: str) -> Dict:
        """Load rules from JSON file."""
        with open(rules_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _initialize_flowcharts(self):
        
        self.pe_flowchart = {
            
            "Q1": Question(
                text="Do you ejaculate within one minute of penetration or before you want to?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": "Q2",
                    "No": {"diagnosis": Diagnosis(
                        category="No Concern",
                        causes="Your ejaculation timing appears to be within normal range.",
                        specialist="No referral needed."
                    )}
                }
            ),
            "Q2": Question(
                text="Has this issue been present since your first sexual experience, or did it start later?",
                options=["Lifelong", "Acquired"],
                next_steps={
                    "Lifelong": "Q3",
                    "Acquired": "Q4"
                }
            ),
            
            "Q3": Question(
                text="Have you ever been able to control ejaculation during sex or masturbation?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": "Q5",
                    "No": {"diagnosis": Diagnosis(
                        category="Lifelong PE – likely neurological/genetic",
                        causes="You have experienced this condition since your first sexual experience and have never had control over ejaculation.",
                        specialist="Refer to Psychiatrist"
                    )}
                }
            ),
            "Q4": Question(
                text="Did this issue start suddenly or gradually over time?",
                options=["Suddenly", "Gradually"],
                next_steps={
                    "Suddenly": "Q6",
                    "Gradually": "Q7"
                }
            ),
            "Q5": Question(
                text="Do you often worry about how well you'll perform during sex, even before it begins?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": "Q6",
                    "No": "Q8"
                }
            ),
            "Q6": Question(
                text="Do you notice racing thoughts, overthinking, or fear of disappointing your partner?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Performance Anxiety",
                        causes="Your symptoms indicate significant anxiety and stress around sexual performance.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": "Q9"
                }
            ),
            "Q7": Question(
                text="Have you been experiencing chronic stress, burnout, or emotional pressure recently?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Psychological PE – stress-related",
                        causes="Your condition appears to be related to chronic stress and emotional pressure.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": "Q10"
                }
            ),
            
            "Q8": Question(
                text="Do you have any diagnosed health conditions like prostatitis, diabetes, or thyroid issues?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Acquired PE – medical basis",
                        causes="Your condition may be related to underlying medical conditions.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q11"
                }
            ),
            "Q9": Question(
                text="Do you frequently masturbate or watch porn (more than 4–5 times a week)?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Sensory Overload / Desensitisation",
                        causes="Frequent masturbation and porn consumption may be affecting your sexual response.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": "Q12"
                }
            ),
            "Q10": Question(
                text="Do you feel a very strong sensation or tingling in the penis during sex that's hard to control?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Penile Hypersensitivity",
                        causes="You may be experiencing heightened penile sensitivity.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": "Q13"
                }
            ),
            "Q11": Question(
                text="Do you often masturbate by rubbing against a bed, pillow, or surface (not using your hand)?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Atypical Sensory Conditioning",
                        causes="Your masturbation technique may be contributing to the condition.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": "Q14"
                }
            ),
            "Q12": Question(
                text="Do you feel a burning, pain, or discomfort during or after ejaculation?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Genital Infection or Prostatitis",
                        causes="Your symptoms suggest possible infection or inflammation.",
                        specialist="Refer to Venereologist/Andrologist"
                    )},
                    "No": "Q15"
                }
            ),
            #
            "Q13": Question(
                text="Are you circumcised or have foreskin issues like phimosis or balanitis?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Foreskin-Related PE",
                        causes="Your condition may be related to foreskin issues.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q16"
                }
            ),
            "Q14": Question(
                text="Do you have a history of mood swings, impulsivity, or depression?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Low Serotonin / Mood-based PE",
                        causes="Your condition may be related to mood disorders or serotonin levels.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": "Q17"
                }
            ),
            "Q15": Question(
                text="Do you ejaculate even before penetration or with minimal stimulation?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Hyperactive Ejaculatory Reflex",
                        causes="You may have a heightened ejaculatory reflex.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": "Q16"
                }
            ),
            "Q16": Question(
                text="Are you on medications like antidepressants or BP medications?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Medication-Induced PE",
                        causes="Your condition may be related to your current medications.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": "Q17"
                }
            ),
            "Q17": Question(
                text="Do you masturbate with a very tight grip that normal sex doesn't match? (Death Grip Syndrome)",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Death Grip Syndrome",
                        causes="Your masturbation technique may be affecting your sexual response.",
                        specialist="Refer to Psychiatrist"
                    )},
                    "No": {"diagnosis": Diagnosis(
                        category="Non-specific PE – likely mixed factors",
                        causes="Your condition appears to have multiple contributing factors.",
                        specialist="Refer to Psychiatrist"
                    )}
                }
            )
        }

        
        self.ed_flowchart = {
            "Q1": Question(
                text="Are you experiencing difficulty in getting or maintaining an erection?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": "Q2",
                    "No": {"diagnosis": Diagnosis(
                        category="No Concern",
                        causes="You are not experiencing erectile dysfunction.",
                        specialist="No referral needed."
                    )}
                }
            ),
            "Q2": Question(
                text="Did this issue start suddenly or gradually over time?",
                options=["Suddenly", "Gradually"],
                next_steps={
                    "Suddenly": "Q3",
                    "Gradually": "Q4"
                }
            ),
            "Q3": Question(
                text="Have you or your partner been engaging in timed intercourse for pregnancy planning?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Performance Anxiety",
                        causes="The pressure of timed intercourse may be causing performance anxiety.",
                        specialist="Refer to Psychiatrist/Sexologist"
                    )},
                    "No": "Q5"
                }
            ),
            "Q4": Question(
                text="Do you have any medical conditions (e.g., diabetes, high blood pressure, heart disease)?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Vascular ED",
                        causes="Your ED may be related to underlying medical conditions affecting blood flow.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q5"
                }
            ),
            "Q5": Question(
                text="Have you been feeling stressed, anxious, or facing relationship issues?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Psychological ED",
                        causes="Your ED appears to be related to psychological factors or relationship issues.",
                        specialist="Refer to Psychiatrist/Sexologist"
                    )},
                    "No": "Q6"
                }
            ),
            "Q6": Question(
                text="Do you still experience morning erections?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": "Q7",
                    "No": "Q8"
                }
            ),
            "Q7": Question(
                text="Do you feel highly anxious or nervous before sex?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Performance Anxiety",
                        causes="Your symptoms indicate significant anxiety around sexual performance.",
                        specialist="Refer to Psychiatrist/Sexologist"
                    )},
                    "No": "Q9"
                }
            ),
            "Q8": Question(
                text="Have you noticed a decrease in sex drive (libido)?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": "Q10",
                    "No": "Q11"
                }
            ),
            "Q9": Question(
                text="Do you smoke, drink excessively, or have an inactive lifestyle?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Lifestyle-induced ED",
                        causes="Your ED may be related to lifestyle factors.",
                        specialist="Refer to Psychiatrist/Sexologist"
                    )},
                    "No": "Q10"
                }
            ),
            "Q10": Question(
                text="Have you experienced weight gain, fatigue, or reduced muscle mass?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Hormonal ED",
                        causes="Your symptoms suggest possible hormonal imbalance or low testosterone.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q11"
                }
            ),
            "Q11": Question(
                text="Are you taking any medications (e.g., antidepressants, BP meds)?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Medication-induced ED",
                        causes="Your ED may be a side effect of your current medications.",
                        specialist="Refer to Psychiatrist/Sexologist"
                    )},
                    "No": "Q12"
                }
            ),
            "Q12": Question(
                text="Have you had any pelvic or genital injuries or surgeries?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Post-surgical or Nerve-related ED",
                        causes="Your ED may be related to previous injuries or surgeries.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q13"
                }
            ),
            "Q13": Question(
                text="Do you experience penile curvature, pain, or discomfort during erection?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Peyronie's Disease",
                        causes="Your symptoms suggest possible Peyronie's Disease.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q14"
                }
            ),
            "Q14": Question(
                text="Have you had penile infections like balanitis (pain, redness, discharge)?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Inflammation-related ED",
                        causes="Your ED may be related to inflammation or infection.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q15"
                }
            ),
            "Q15": Question(
                text="Do you snore loudly, feel tired during the day, or wake up gasping at night?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Sleep Apnea-induced ED",
                        causes="Your ED may be related to sleep apnea.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q16"
                }
            ),
            "Q16": Question(
                text="Do you have an autoimmune condition or frequent joint pain/inflammation?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Autoimmune-linked ED",
                        causes="Your ED may be related to autoimmune conditions or chronic inflammation.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q17"
                }
            ),
            "Q17": Question(
                text="Do you have groin, lower abdominal or perineal pain along with erection difficulty?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Pelvic Floor Dysfunction",
                        causes="Your symptoms suggest possible pelvic floor dysfunction.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": "Q18"
                }
            ),
            "Q18": Question(
                text="Do you frequently masturbate with a tight grip that intercourse doesn't match?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Death Grip Syndrome",
                        causes="Your masturbation technique may be affecting your sexual response.",
                        specialist="Refer to Psychosexual Therapist/Sexologist"
                    )},
                    "No": "Q19"
                }
            ),
            "Q19": Question(
                text="Have you used anabolic steroids, recreational drugs, or any other substances that could impact sexual function?",
                options=["Yes", "No"],
                next_steps={
                    "Yes": {"diagnosis": Diagnosis(
                        category="Drug-induced ED",
                        causes="Your ED may be related to substance use.",
                        specialist="Refer to Andrologist"
                    )},
                    "No": {"diagnosis": Diagnosis(
                        category="Non-specific ED",
                        causes="Your ED appears to have multiple or unclear contributing factors.",
                        specialist="Refer to Psychiatrist/Sexologist"
                    )}
                }
            )
        }

        
        self.hindi_translations = {
            
            "Do you ejaculate within one minute of penetration or before you want to?": "Kya aap penetration ke ek minute ke andar ya jab aap chahte hain usse pehle ejaculate ho jata hai?",
            "Has this issue been present since your first sexual experience, or did it start later?": "Kya ye problem first sexual experience se hai, ya baad mein start hui?",
            "Have you ever been able to control ejaculation during sex or masturbation?": "Kya aap kabhi sex ya masturbation ke time ejaculation ko control kar paye hain?",
            "Did this issue start suddenly or gradually over time?": "Kya ye problem suddenly start hui ya gradually time ke sath?",
            "Do you often worry about how well you'll perform during sex, even before it begins?": "Kya aap sex shuru hone se pehle hi performance ki tension lete hain?",
            "Do you notice racing thoughts, overthinking, or fear of disappointing your partner?": "Kya aap racing thoughts, overthinking ya partner ko disappoint karne ka fear feel karte hain?",
            "Have you been experiencing chronic stress, burnout, or emotional pressure recently?": "Kya aap chronic stress, burnout, ya emotional pressure feel kar rahe hain?",
            "Do you have any diagnosed health conditions like prostatitis, diabetes, or thyroid issues?": "Kya doctor ne aapko koi condition diagnose ki hai jaise prostatitis, diabetes, ya thyroid issues?",
            "Do you frequently masturbate or watch porn (more than 4–5 times a week)?": "Kya aap frequently masturbate karte hain ya porn dekhte hain (4-5 times per week se zyada)?",
            "Do you feel a very strong sensation or tingling in the penis during sex that's hard to control?": "Kya sex ke time penis mein bahut strong sensation ya tingling hoti hai jo control karna mushkil hota hai?",
            "Do you often masturbate by rubbing against a bed, pillow, or surface (not using your hand)?": "Kya aap often bed, pillow, ya surface pe rub karke masturbate karte hain (hand use nahi karte)?",
            "Do you feel a burning, pain, or discomfort during or after ejaculation?": "Kya ejaculation ke time ya baad mein burning, pain, ya discomfort hota hai?",
            "Are you circumcised or have foreskin issues like phimosis or balanitis?": "Kya aap circumcised hain ya foreskin mein koi issues hain jaise phimosis ya balanitis?",
            "Do you have a history of mood swings, impulsivity, or depression?": "Kya aapko mood swings, impulsivity, ya depression ki history hai?",
            "Do you ejaculate even before penetration or with minimal stimulation?": "Kya penetration se pehle hi ya minimal stimulation se ejaculation ho jata hai?",
            "Are you on medications like antidepressants or BP medications?": "Kya aap koi dawai le rahe hain jaise depression ki ya BP ki dawai?",
            "Do you masturbate with a very tight grip that normal sex doesn't match? (Death Grip Syndrome)": "Kya aap masturbation ke time bahut tight grip use karte hain jo normal sex ke time match nahi karta? (Death Grip Syndrome)",

            
            "Are you experiencing difficulty in getting or maintaining an erection?": "Kya apko erection laane me ya barkaraar rakhne me dikkat hoti hai?",
            "Have you or your partner been engaging in timed intercourse for pregnancy planning?": "Kya aap ya aapki partner pregnancy planning ke liye timed intercourse kar rahe hain?",
            "Do you have any medical conditions (e.g., diabetes, high blood pressure, heart disease)?": "Kya aapko koi medical conditions hain (jaise diabetes, high BP, heart disease)?",
            "Have you been feeling stressed, anxious, or facing relationship issues?": "Kya aap stressed, anxious feel kar rahe hain, ya relationship issues face kar rahe hain?",
            "Do you still experience morning erections?": "Kya aap abhi bhi morning erections experience karte hain?",
            "Do you feel highly anxious or nervous before sex?": "Kya sex se pehle aap highly anxious ya nervous feel karte hain?",
            "Have you noticed a decrease in sex drive (libido)?": "Kya aapne sex drive (libido) mein decrease notice kiya hai?",
            "Do you smoke, drink excessively, or have an inactive lifestyle?": "Kya aap smoke karte hain, excessive drinking karte hain, ya inactive lifestyle hai?",
            "Have you experienced weight gain, fatigue, or reduced muscle mass?": "Kya aapne weight gain, fatigue, ya reduced muscle mass experience kiya hai?",
            "Have you had any pelvic or genital injuries or surgeries?": "Kya aapke pelvic ya genital area mein koi injuries ya surgeries hui hain?",
            "Do you experience penile curvature, pain, or discomfort during erection?": "Kya erection ke time penile curvature, pain, ya discomfort hota hai?",
            "Have you had penile infections like balanitis (pain, redness, discharge)?": "Kya aapko penile infections hui hain jaise balanitis (pain, redness, discharge)?",
            "Do you snore loudly, feel tired during the day, or wake up gasping at night?": "Kya aap zor se kharrate lete hain, din mein tired feel karte hain, ya raat mein saans phulne se uth jate hain?",
            "Do you have an autoimmune condition or frequent joint pain/inflammation?": "Kya aapko autoimmune condition ya frequent joint pain/inflammation hai?",
            "Do you have groin, lower abdominal or perineal pain along with erection difficulty?": "Kya erection difficulty ke sath jangha ke beech mein, pet ke niche ya guptang ke aas-paas dard hai?",
            "Have you used anabolic steroids, recreational drugs, or any other substances?": "Kya aapne body banane ki dawa, nashe wali dawayein, ya koi aur substances use kiye hain?",
            "Do you frequently masturbate with a tight grip that intercourse doesn't match?": "Kya aap masturbation ke time bahut tight grip use karte hain jo normal sex ke time match nahi karta?",
            "Are you taking any medications (e.g., antidepressants, BP meds)?": "Kya aap koi dawai le rahe hain jaise depression ki ya BP ki dawai?",
            "Have you used anabolic steroids, recreational drugs, or any other substances that could impact sexual function?": "Kya aapne body banane ki dawa, nashe wali dawayein, ya koi aur cheez li hai jo sexual function ko affect kar sakti hai?",

            
            "Yes": "Yes",
            "No": "No",
            "Suddenly": "Suddenly",
            "Gradually": "Gradually",
            "Lifelong": "Lifelong",
            "Acquired": "Acquired",

            
            "No Concern": "No Concern",
            "Performance Anxiety": "Performance Anxiety",
            "Psychological PE": "Psychological PE",
            "Vascular ED": "Vascular ED",
            "Hormonal ED": "Hormonal ED",
            "Lifestyle-induced ED": "Lifestyle-induced ED",
            "Drug-induced ED": "Drug-induced ED",
            "Peyronie's Disease": "Peyronie's Disease",
            "Sleep Apnea-induced ED": "Sleep Apnea-induced ED",
            "Pelvic Floor Dysfunction": "Pelvic Floor Dysfunction",
            "Death Grip Syndrome": "Death Grip Syndrome",
            "Non-specific ED": "Non-specific ED",
            "Medication-Induced PE": "Medication-Induced PE",
            "Genital Infection or Prostatitis": "Genital Infection ya Prostatitis",
            "Foreskin-Related PE": "Foreskin-Related PE",
            "Penile Hypersensitivity": "Penile Hypersensitivity",
            "Atypical Sensory Conditioning": "Atypical Sensory Conditioning",

            
            "No referral needed": "No referral needed",
            "Refer to Psychiatrist": "Refer to Psychiatrist",
            "Refer to Andrologist": "Refer to Andrologist",
            "Refer to Urologist": "Refer to Urologist",
            "Refer to Endocrinologist": "Refer to Endocrinologist",
            "Refer to Sleep Specialist": "Refer to Sleep Specialist",
            "Refer to Rheumatologist": "Refer to Rheumatologist",
            "Refer to Pelvic Floor Specialist": "Refer to Pelvic Floor Specialist",
            "Refer to Addiction Specialist": "Refer to Addiction Specialist",
            "Refer to Venereologist/Andrologist": "Refer to Venereologist/Andrologist",
            "Refer to Psychiatrist/Sexologist": "Refer to Psychiatrist/Sexologist",
            "Refer to Psychosexual Therapist/Sexologist": "Refer to Psychosexual Therapist/Sexologist",

            \
            "Choose your concern": "Choose your concern"
        }

    def get_language_options(self) -> List[str]:
        """Return available language options."""
        return ["English", "Hindi"]
    
    def set_language(self, language: str) -> None:
        """Set the chatbot language."""
        self.current_language = "en" if language == "English" else "hi"
    
    def get_language_selection_text(self) -> str:
        """Get the language selection text."""
        return "Select Language / भाषा चुनें"
    
    def get_concern_options(self) -> List[str]:
        """Get available concern options in current language."""
        
        return ["Premature Ejaculation", "Erectile Dysfunction"]
    
    def set_concern(self, concern: str) -> None:
        """Set the user's selected concern."""
        self.current_concern = concern
        if concern in ["Premature Ejaculation", "Jaldi discharge ho jaana"]:
            self.current_question = "Q1"
            self.current_flowchart = self.pe_flowchart
        else:
            self.current_question = "Q1"
            self.current_flowchart = self.ed_flowchart
        self.analysis_points = []
    
    def _translate_question(self, question: Question) -> Question:
        if self.current_language == "en":
            return question
        
        translated_text = self.hindi_translations.get(question.text, question.text)
        translated_options = [self.hindi_translations.get(opt, opt) for opt in question.options]
        
        return Question(
            text=translated_text,
            options=translated_options,
            next_steps=question.next_steps
        )

    def _translate_answer_to_english(self, hindi_answer: str) -> str:
        """Translate Hindi answer back to English for internal logic."""
        
        reverse_translations = {v: k for k, v in self.hindi_translations.items()}
        return reverse_translations.get(hindi_answer, hindi_answer)

    def get_next_question(self, answer: Optional[str] = None) -> Union[Dict, Question]:
        if answer and self.current_question:
            
            current_q = self.current_flowchart[self.current_question]
            translated_q = self._translate_question(current_q)
            self.chat_history.append({
                "question": translated_q.text,
                "answer": answer
            })
            
            
            if self.current_language == "hi":
                answer = self._translate_answer_to_english(answer)
            
        
            next_step = current_q.next_steps[answer]
            
            
            if isinstance(next_step, dict) and "diagnosis" in next_step:
                diagnosis = next_step["diagnosis"]
                translated_category = self.hindi_translations.get(diagnosis.category, diagnosis.category) if self.current_language == "hi" else diagnosis.category
                translated_causes = self.hindi_translations.get(diagnosis.causes, diagnosis.causes) if self.current_language == "hi" else diagnosis.causes
                translated_specialist = self.hindi_translations.get(diagnosis.specialist, diagnosis.specialist) if self.current_language == "hi" else diagnosis.specialist
                
                return {
                    "output_format": "diagnosis",
                    "sections": {
                        "title": "# Final Analysis",
                        "category": f"## {translated_category}",
                        "causes_header": "## Primary Causes",
                    "causes": translated_causes,
                        "specialist_header": "## Recommended Specialist",
                    "specialist": translated_specialist
                    }
                }
            
            
            self.current_question = next_step
        
        
        question = self.current_flowchart[self.current_question]
        translated_q = self._translate_question(question)
        
        
        return {
            "text": translated_q.text,
            "options": translated_q.options
        }
    
    def compile_final_analysis(self) -> Dict:
        """Generate comprehensive final analysis based on all responses."""
        if not self.analysis_points:
            
            if self.current_concern == "ed":
                return self.rules["final_analysis"]["ed"][self.current_language]["mixed"]
            return self.rules["final_analysis"]["pe"][self.current_language]["nonspecific"]
        
        
        primary_issue = max(set(self.analysis_points), key=self.analysis_points.count)
        analysis = self.rules["final_analysis"][self.current_concern][self.current_language].get(primary_issue)
        
        if not analysis:
            if self.current_concern == "ed":
                return self.rules["final_analysis"]["ed"][self.current_language]["mixed"]
            return self.rules["final_analysis"]["pe"][self.current_language]["nonspecific"]
        
        
        other_issues = set(self.analysis_points) - {primary_issue}
        if other_issues:
            additional_causes = []
            for issue in other_issues:
                if issue_analysis := self.rules["final_analysis"][self.current_concern][self.current_language].get(issue):
                    additional_causes.append(issue_analysis["causes"])
            
            if additional_causes:
                analysis["additional_factors"] = additional_causes
        
        return analysis
    
    def reset(self) -> None:
        """Reset the chatbot state."""
        self.current_language = "en"
        self.current_concern = None
        self.chat_history = []
        self.current_question = None
        self.analysis_points = [] 