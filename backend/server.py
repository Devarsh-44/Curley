from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
import json
import uuid
from collections import Counter
import re

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Medical data - comprehensive dataset based on provided structure
MEDICAL_DATA = [
    {
        "id": str(uuid.uuid4()),
        "disease": "Fungal infection",
        "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions", "dischromic_patches"],
        "description": "A fungal infection is a disease caused by fungus. Common types include athlete's foot, ringworm, and yeast infections.",
        "precautions": ["bath twice", "use detol or neem in bathing water", "keep infected area dry", "use clean cloths"],
        "medicines": ["antifungal cream", "fluconazole", "terbinafine", "itraconazole"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Allergy",
        "symptoms": ["continuous_sneezing", "shivering", "chills", "watering_from_eyes"],
        "description": "An allergy is a reaction by your immune system to something that does not bother most other people.",
        "precautions": ["apply sunscreen", "avoid dust", "avoid pollen", "keep windows closed"],
        "medicines": ["antihistamine", "cetirizine", "loratadine", "nasal decongestant"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "GERD",
        "symptoms": ["stomach_pain", "acidity", "ulcers_on_tongue", "vomiting", "cough", "chest_pain"],
        "description": "Gastroesophageal reflux disease (GERD) occurs when stomach acid frequently flows back into the tube connecting your mouth and stomach.",
        "precautions": ["avoid fatty spicy food", "avoid lying down after eating", "maintain healthy weight", "limit caffeine"],
        "medicines": ["omeprazole", "lansoprazole", "ranitidine", "antacids"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Chronic cholestasis",
        "symptoms": ["itching", "vomiting", "yellowish_skin", "nausea", "loss_of_appetite", "abdominal_pain"],
        "description": "Chronic cholestasis is a condition where bile flow from the liver is reduced or stopped.",
        "precautions": ["cold baths", "anti itch medicine", "avoid fatty foods", "small frequent meals"],
        "medicines": ["ursodeoxycholic acid", "cholestyramine", "rifampin", "naltrexone"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Drug Reaction",
        "symptoms": ["itching", "skin_rash", "burning_micturition", "spotting_urination"],
        "description": "An adverse drug reaction is an injury caused by taking medication.",
        "precautions": ["stop irritation", "consult nearest hospital", "stop taking drug", "follow up"],
        "medicines": ["antihistamine", "corticosteroids", "epinephrine", "supportive care"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Peptic ulcer disease",
        "symptoms": ["vomiting", "indigestion", "loss_of_appetite", "abdominal_pain", "passage_of_gases"],
        "description": "Peptic ulcer disease refers to painful sores or ulcers in the lining of the stomach or first part of the small intestine.",
        "precautions": ["avoid fatty spicy food", "consume probiotic food", "eliminate milk", "limit alcohol"],
        "medicines": ["proton pump inhibitors", "antibiotics", "bismuth subsalicylate", "sucralfate"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "AIDS",
        "symptoms": ["muscle_wasting", "patches_in_throat", "high_fever", "extra_marital_contacts"],
        "description": "Acquired immunodeficiency syndrome (AIDS) is a chronic, potentially life-threatening condition caused by HIV.",
        "precautions": ["avoid open cuts", "wear ppe if possible", "consult doctor", "follow up"],
        "medicines": ["antiretroviral therapy", "zidovudine", "efavirenz", "tenofovir"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Diabetes",
        "symptoms": ["fatigue", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level", "blurred_and_distorted_vision", "obesity", "excessive_hunger"],
        "description": "Diabetes is a group of metabolic disorders characterized by a high blood sugar level over a prolonged period of time.",
        "precautions": ["have balanced diet", "exercise", "consult doctor", "follow up"],
        "medicines": ["metformin", "insulin", "glipizide", "glyburide"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Gastroenteritis",
        "symptoms": ["vomiting", "sunken_eyes", "dehydration", "diarrhoea"],
        "description": "Gastroenteritis is inflammation of the lining of the intestines caused by a virus, bacteria or parasites.",
        "precautions": ["stop eating solid food for while", "try to take liquid", "rest", "ease back into eating"],
        "medicines": ["oral rehydration salts", "zinc supplements", "probiotics", "loperamide"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Bronchial Asthma",
        "symptoms": ["fatigue", "cough", "high_fever", "breathlessness", "family_history", "mucoid_sputum"],
        "description": "Bronchial asthma is a lung disease that makes it hard to breathe when the airways become inflamed and narrowed.",
        "precautions": ["switch to loose cloothing", "take deep breaths", "get away from trigger", "seek help"],
        "medicines": ["albuterol", "beclomethasone", "montelukast", "theophylline"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Hypertension",
        "symptoms": ["headache", "chest_pain", "dizziness", "loss_of_balance", "lack_of_concentration"],
        "description": "Hypertension (high blood pressure) is a condition in which the force of the blood against the artery walls is too high.",
        "precautions": ["meditation", "salt baths", "reduce stress", "get proper sleep"],
        "medicines": ["amlodipine", "lisinopril", "hydrochlorothiazide", "metoprolol"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Migraine",
        "symptoms": ["acidity", "indigestion", "headache", "blurred_and_distorted_vision", "excessive_hunger", "stiff_neck", "depression", "irritability", "visual_disturbances"],
        "description": "A migraine is a headache that can cause severe throbbing pain or a pulsing sensation, usually on one side of the head.",
        "precautions": ["meditation", "reduce stress", "use poloroid glasses in sun", "consult doctor"],
        "medicines": ["sumatriptan", "rizatriptan", "topiramate", "propranolol"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Cervical spondylosis",
        "symptoms": ["back_pain", "weakness_in_limbs", "neck_pain", "dizziness", "loss_of_balance"],
        "description": "Cervical spondylosis is a general term for age-related wear and tear affecting the spinal disks in your neck.",
        "precautions": ["use heating pad or cold pack", "exercise", "take otc pain reliver", "consult doctor"],
        "medicines": ["ibuprofen", "naproxen", "muscle relaxants", "gabapentin"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Paralysis (brain hemorrhage)",
        "symptoms": ["vomiting", "headache", "weakness_of_one_body_side", "altered_sensorium"],
        "description": "Paralysis is the loss of muscle function in part of your body, often caused by brain hemorrhage.",
        "precautions": ["massage", "eat healthy", "exercise", "consult doctor"],
        "medicines": ["physiotherapy", "speech therapy", "occupational therapy", "anticoagulants"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Jaundice",
        "symptoms": ["itching", "vomiting", "fatigue", "weight_loss", "high_fever", "headache", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "constipation", "abdominal_pain", "diarrhoea", "mild_fever", "yellowing_of_eyes"],
        "description": "Jaundice is a condition in which the skin, whites of the eyes and mucous membranes turn yellow because of a high level of bilirubin.",
        "precautions": ["drink plenty of water", "consume milk thistle", "eat fruits and high fiberous food", "medication"],
        "medicines": ["ursodeoxycholic acid", "phenobarbital", "cholestyramine", "vitamin K"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Malaria",
        "symptoms": ["chills", "vomiting", "high_fever", "sweating", "headache", "nausea", "diarrhoea", "muscle_pain"],
        "description": "Malaria is a disease caused by a parasite that commonly infects a certain type of mosquito which feeds on humans.",
        "precautions": ["consult nearest hospital", "avoid oily food", "avoid non veg food", "keep mosquitos out"],
        "medicines": ["artemether-lumefantrine", "chloroquine", "doxycycline", "mefloquine"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Chicken pox",
        "symptoms": ["itching", "skin_rash", "fatigue", "lethargy", "high_fever", "headache", "loss_of_appetite", "mild_fever"],
        "description": "Chickenpox is a highly contagious disease caused by the varicella-zoster virus (VZV).",
        "precautions": ["use neem in bathing", "consume neem leaves", "take vaccine", "avoid public places"],
        "medicines": ["acyclovir", "valacyclovir", "calamine lotion", "paracetamol"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Dengue",
        "symptoms": ["skin_rash", "chills", "joint_pain", "vomiting", "fatigue", "high_fever", "headache", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "malaise", "muscle_pain", "red_spots_over_body"],
        "description": "Dengue is a mosquito-borne tropical disease caused by the dengue virus.",
        "precautions": ["drink papaya leaf juice", "avoid fatty spicy food", "keep mosquitos away", "keep hydrated"],
        "medicines": ["paracetamol", "oral rehydration therapy", "platelet transfusion", "supportive care"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Typhoid",
        "symptoms": ["chills", "vomiting", "fatigue", "high_fever", "headache", "nausea", "constipation", "abdominal_pain", "diarrhoea", "toxic_look_(typhos)", "belly_pain"],
        "description": "Typhoid fever is a bacterial infection due to a specific type of Salmonella that causes symptoms.",
        "precautions": ["eat high calorie vegitables", "antiboitic therapy", "consult doctor", "medication"],
        "medicines": ["ciprofloxacin", "azithromycin", "ceftriaxone", "chloramphenicol"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "hepatitis A",
        "symptoms": ["joint_pain", "vomiting", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "diarrhoea", "mild_fever", "yellowing_of_eyes", "muscle_pain"],
        "description": "Hepatitis A is a viral infection that causes liver inflammation and damage.",
        "precautions": ["consult nearest hospital", "wash hands through", "avoid fatty spicy food", "medication"],
        "medicines": ["supportive care", "rest", "adequate hydration", "hepatitis A vaccine"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Hepatitis B",
        "symptoms": ["itching", "fatigue", "lethargy", "yellowish_skin", "dark_urine", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes"],
        "description": "Hepatitis B is a viral infection that attacks the liver and can cause both acute and chronic disease.",
        "precautions": ["consult nearest hospital", "vaccination", "eat healthy", "medication"],
        "medicines": ["tenofovir", "entecavir", "lamivudine", "interferon alpha"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Hepatitis C",
        "symptoms": ["fatigue", "yellowish_skin", "nausea", "loss_of_appetite", "yellowing_of_eyes", "family_history"],
        "description": "Hepatitis C is a viral infection caused by the hepatitis C virus (HCV) that attacks the liver.",
        "precautions": ["consult nearest hospital", "vaccination", "eat healthy", "medication"],
        "medicines": ["sofosbuvir", "ledipasvir", "daclatasvir", "ribavirin"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Hepatitis D",
        "symptoms": ["joint_pain", "vomiting", "fatigue", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes"],
        "description": "Hepatitis D is a liver infection caused by the hepatitis D virus (HDV), also called the delta virus.",
        "precautions": ["consult nearest hospital", "vaccination", "eat healthy", "medication"],
        "medicines": ["pegylated interferon", "supportive care", "liver transplant", "antiviral therapy"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Hepatitis E",
        "symptoms": ["joint_pain", "vomiting", "fatigue", "high_fever", "yellowish_skin", "dark_urine", "nausea", "loss_of_appetite", "abdominal_pain", "yellowing_of_eyes", "acute_liver_failure", "coma", "stomach_bleeding"],
        "description": "Hepatitis E is a liver disease caused by infection with a virus known as hepatitis E virus (HEV).",
        "precautions": ["stop alcohol consumption", "rest", "consult doctor", "medication"],
        "medicines": ["supportive care", "rest", "adequate nutrition", "ribavirin"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Alcoholic hepatitis",
        "symptoms": ["vomiting", "yellowish_skin", "abdominal_pain", "swelling_of_stomach", "distention_of_abdomen", "history_of_alcohol_consumption", "fluid_overload"],
        "description": "Alcoholic hepatitis is inflammation of the liver caused by drinking alcohol.",
        "precautions": ["stop alcohol consumption", "consult doctor", "medication", "follow up"],
        "medicines": ["corticosteroids", "pentoxifylline", "nutritional support", "liver transplant"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Tuberculosis",
        "symptoms": ["chills", "vomiting", "fatigue", "weight_loss", "cough", "high_fever", "breathlessness", "sweating", "loss_of_appetite", "mild_fever", "yellowing_of_eyes", "swelled_lymph_nodes", "malaise", "phlegm", "chest_pain", "blood_in_sputum"],
        "description": "Tuberculosis (TB) is a potentially serious infectious disease that mainly affects the lungs.",
        "precautions": ["cover mouth", "consult doctor", "medication", "rest"],
        "medicines": ["isoniazid", "rifampin", "ethambutol", "pyrazinamide"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Common Cold",
        "symptoms": ["continuous_sneezing", "chills", "fatigue", "cough", "high_fever", "headache", "swelled_lymph_nodes", "malaise", "phlegm", "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion", "chest_pain", "loss_of_smell", "muscle_pain"],
        "description": "The common cold is a viral infectious disease of the upper respiratory tract that primarily affects the respiratory mucosa.",
        "precautions": ["drink vitamin c rich drinks", "take vapour", "avoid cold food", "keep fever in check"],
        "medicines": ["decongestants", "cough suppressants", "pain relievers", "antihistamines"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Pneumonia",
        "symptoms": ["chills", "fatigue", "cough", "high_fever", "breathlessness", "sweating", "malaise", "phlegm", "chest_pain", "fast_heart_rate", "rusty_sputum"],
        "description": "Pneumonia is an infection that inflames air sacs in one or both lungs, which may fill with fluid.",
        "precautions": ["consult doctor", "medication", "rest", "follow up"],
        "medicines": ["antibiotics", "cough medicine", "fever reducers", "pain relievers"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Dimorphic hemmorhoids(piles)",
        "symptoms": ["constipation", "pain_during_bowel_movements", "pain_in_anal_region", "bloody_stool", "irritation_in_anus"],
        "description": "Hemorrhoids are swollen veins in the lower part of the rectum and anus.",
        "precautions": ["avoid fatty spicy food", "consume witch hazel", "warm bath with epsom salt", "consume alovera juice"],
        "medicines": ["topical treatments", "oral pain relievers", "stool softeners", "suppositories"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Heart attack",
        "symptoms": ["vomiting", "breathlessness", "sweating", "chest_pain"],
        "description": "A heart attack occurs when the flow of blood to the heart is blocked.",
        "precautions": ["call ambulance", "chew or swallow asprin", "keep calm", "seek help"],
        "medicines": ["aspirin", "clopidogrel", "atorvastatin", "metoprolol"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Varicose veins",
        "symptoms": ["fatigue", "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels", "prominent_veins_on_calf"],
        "description": "Varicose veins are larger, swollen blood vessels that turn and twist just under the skin of the legs.",
        "precautions": ["lie down flat and raise the leg high", "use oinments", "use vein compression", "dont stand still for long"],
        "medicines": ["compression stockings", "sclerotherapy", "laser treatment", "vein stripping"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Hypothyroidism",
        "symptoms": ["fatigue", "weight_gain", "cold_hands_and_feets", "mood_swings", "loss_of_balance", "dizziness", "depression", "irritability", "abnormal_menstruation"],
        "description": "Hypothyroidism is a condition in which the thyroid gland doesn't produce enough thyroid hormone.",
        "precautions": ["reduce stress", "exercise", "eat healthy", "get proper sleep"],
        "medicines": ["levothyroxine", "liothyronine", "armour thyroid", "nature-throid"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Hyperthyroidism",
        "symptoms": ["fatigue", "mood_swings", "weight_loss", "restlessness", "sweating", "diarrhoea", "fast_heart_rate", "excessive_hunger", "muscle_weakness", "irritability", "abnormal_menstruation"],
        "description": "Hyperthyroidism occurs when the thyroid gland produces too much thyroid hormone.",
        "precautions": ["eat healthy", "massage", "use lemon balm", "take radioactive iodine treatment"],
        "medicines": ["methimazole", "propylthiouracil", "radioactive iodine", "beta blockers"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Hypoglycemia",
        "symptoms": ["vomiting", "fatigue", "anxiety", "sweating", "headache", "nausea", "blurred_and_distorted_vision", "excessive_hunger", "drying_and_tingling_lips", "slurred_speech"],
        "description": "Hypoglycemia is a condition in which your blood sugar (glucose) level is lower than normal.",
        "precautions": ["lie down on side", "check in pulse", "drink sugary drinks", "consult doctor"],
        "medicines": ["glucose tablets", "glucagon injection", "dextrose", "sugar"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Osteoarthristis",
        "symptoms": ["joint_pain", "neck_pain", "knee_pain", "hip_joint_pain", "swelling_joints", "painful_walking"],
        "description": "Osteoarthritis is the most common form of arthritis, affecting millions of people worldwide.",
        "precautions": ["acetaminophen", "use hot and cold therapy", "try acupuncture", "massage"],
        "medicines": ["acetaminophen", "ibuprofen", "naproxen", "topical analgesics"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Arthritis",
        "symptoms": ["muscle_weakness", "stiff_neck", "swelling_joints", "movement_stiffness", "painful_walking"],
        "description": "Arthritis is inflammation of one or more joints, causing pain and stiffness that can worsen with age.",
        "precautions": ["exercise", "use hot and cold therapy", "try acupuncture", "massage"],
        "medicines": ["NSAIDs", "corticosteroids", "DMARDs", "biologics"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "(vertigo) Paroymsal  Positional Vertigo",
        "symptoms": ["vomiting", "headache", "nausea", "spinning_movements", "loss_of_balance", "unsteadiness"],
        "description": "Benign paroxysmal positional vertigo (BPPV) is one of the most common causes of vertigo.",
        "precautions": ["lie down", "avoid sudden change in body", "avoid abrupt head movment", "relax"],
        "medicines": ["meclizine", "dimenhydrinate", "prochlorperazine", "betahistine"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Acne",
        "symptoms": ["skin_rash", "pus_filled_pimples", "blackheads", "scurring"],
        "description": "Acne is a skin condition that occurs when your hair follicles become plugged with oil and dead skin cells.",
        "precautions": ["bath twice", "avoid fatty spicy food", "drink plenty of water", "avoid too many products"],
        "medicines": ["benzoyl peroxide", "retinoids", "antibiotics", "salicylic acid"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Urinary tract infection",
        "symptoms": ["burning_micturition", "spotting_urination", "foul_smell_of_urine", "continuous_feel_of_urine"],
        "description": "A urinary tract infection (UTI) is an infection in any part of your urinary system.",
        "precautions": ["drink plenty of water", "increase vitamin c intake", "drink cranberry juice", "take probiotics"],
        "medicines": ["trimethoprim-sulfamethoxazole", "nitrofurantoin", "ciprofloxacin", "fosfomycin"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Psoriasis",
        "symptoms": ["skin_rash", "joint_pain", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails"],
        "description": "Psoriasis is a skin disease that causes red, itchy scaly patches, most commonly on the knees, elbows, trunk and scalp.",
        "precautions": ["wash hands with warm soapy water", "stop bleeding using pressure", "consult doctor", "salt baths"],
        "medicines": ["topical corticosteroids", "vitamin D analogues", "retinoids", "immunosuppressants"]
    },
    {
        "id": str(uuid.uuid4()),
        "disease": "Impetigo",
        "symptoms": ["skin_rash", "high_fever", "blister", "red_sore_around_nose", "yellow_crust_ooze"],
        "description": "Impetigo is a common and highly contagious skin infection that mainly affects infants and children.",
        "precautions": ["soak affected area in warm water", "use antibiotics", "remove scabs with wet compressed cloth", "consult doctor"],
        "medicines": ["topical antibiotics", "oral antibiotics", "mupirocin", "retapamulin"]
    }
]

class SymptomRequest(BaseModel):
    symptoms: List[str]

class DiseasePrediction(BaseModel):
    id: str
    disease: str
    confidence: float
    matching_symptoms: List[str]
    total_symptoms: int
    description: str
    precautions: List[str]
    medicines: List[str]

def normalize_symptom(symptom: str) -> str:
    """Normalize symptom for better matching"""
    return re.sub(r'[^a-zA-Z0-9\s]', '', symptom.lower().strip().replace('_', ' '))

def calculate_confidence(user_symptoms: List[str], disease_symptoms: List[str]) -> tuple:
    """Calculate confidence score and matching symptoms"""
    normalized_user = [normalize_symptom(s) for s in user_symptoms]
    normalized_disease = [normalize_symptom(s) for s in disease_symptoms]
    
    # Exact matches
    exact_matches = []
    for user_sym in normalized_user:
        for disease_sym in normalized_disease:
            if user_sym == disease_sym:
                exact_matches.append(user_sym)
    
    # Partial matches (if symptom contains the user input or vice versa)
    partial_matches = []
    for user_sym in normalized_user:
        for disease_sym in normalized_disease:
            if (user_sym in disease_sym or disease_sym in user_sym) and disease_sym not in exact_matches:
                partial_matches.append(disease_sym)
    
    total_matches = len(exact_matches) + (len(partial_matches) * 0.7)  # Partial matches have 70% weight
    
    if len(normalized_user) == 0:
        return 0.0, []
    
    # Confidence based on percentage of user symptoms matched
    confidence = (total_matches / len(normalized_user)) * 100
    
    # Bonus for having many symptoms match
    if total_matches >= 3:
        confidence += 10
    elif total_matches >= 2:
        confidence += 5
    
    # Cap at 95% for realistic medical prediction
    confidence = min(confidence, 95.0)
    
    return confidence, exact_matches + partial_matches

@app.get("/api/")
async def root():
    return {"message": "Curely 2.0 - Smart Medical Assistant API", "status": "active"}

@app.post("/api/predict-disease")
async def predict_disease(request: SymptomRequest) -> List[DiseasePrediction]:
    """Predict diseases based on symptoms"""
    if not request.symptoms:
        raise HTTPException(status_code=400, detail="No symptoms provided")
    
    predictions = []
    
    for disease_data in MEDICAL_DATA:
        confidence, matching_symptoms = calculate_confidence(request.symptoms, disease_data["symptoms"])
        
        if confidence > 0:  # Only include diseases with some match
            prediction = DiseasePrediction(
                id=disease_data["id"],
                disease=disease_data["disease"],
                confidence=round(confidence, 1),
                matching_symptoms=matching_symptoms,
                total_symptoms=len(disease_data["symptoms"]),
                description=disease_data["description"],
                precautions=disease_data["precautions"],
                medicines=disease_data["medicines"]
            )
            predictions.append(prediction)
    
    # Sort by confidence score
    predictions.sort(key=lambda x: x.confidence, reverse=True)
    
    # Return top 5 predictions
    return predictions[:5]

@app.get("/api/disease/{disease_id}")
async def get_disease_details(disease_id: str):
    """Get detailed information about a specific disease"""
    for disease_data in MEDICAL_DATA:
        if disease_data["id"] == disease_id:
            return disease_data
    
    raise HTTPException(status_code=404, detail="Disease not found")

@app.get("/api/diseases")
async def get_all_diseases():
    """Get list of all diseases"""
    return [{"id": disease["id"], "disease": disease["disease"], "symptoms": disease["symptoms"]} for disease in MEDICAL_DATA]

@app.get("/api/search-diseases")
async def search_diseases(query: str = ""):
    """Search diseases by name"""
    if not query:
        return MEDICAL_DATA
    
    query_lower = query.lower()
    filtered_diseases = [
        disease for disease in MEDICAL_DATA 
        if query_lower in disease["disease"].lower()
    ]
    
    return filtered_diseases

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)