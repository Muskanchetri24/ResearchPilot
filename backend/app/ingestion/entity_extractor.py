import re
from typing import Dict, Any, List
from app.models.entities import MethodEntity, DatasetEntity, TaskEntity


class EntityExtractor:
    """
    NLP Entity Extractor that identifies methods, datasets, tasks, and limitations
    from research paper titles and abstracts.
    """

    KNOWN_METHODS = {
        "vision transformer": ("Vision Transformer", "Transformer"),
        "vit": ("Vision Transformer", "Transformer"),
        "cnn": ("Convolutional Neural Network", "CNN"),
        "resnet": ("ResNet Architecture", "CNN"),
        "u-net": ("U-Net Segmentation Network", "CNN"),
        "unet": ("U-Net Segmentation Network", "CNN"),
        "diffusion": ("Diffusion Model", "Generative AI"),
        "yolo": ("YOLO Detector", "Object Detection"),
        "random forest": ("Random Forest", "Traditional ML"),
        "svm": ("Support Vector Machine", "Traditional ML"),
        "xgboost": ("XGBoost Gradient Boosting", "Traditional ML"),
        "graph neural network": ("Graph Neural Network", "GNN"),
        "gnn": ("Graph Neural Network", "GNN"),
        "contrastive learning": ("Contrastive Self-Supervised Learning", "Self-Supervised"),
        "federated learning": ("Federated Learning", "Distributed AI"),
        "bert": ("BERT Language Model", "Transformer"),
    }

    KNOWN_DATASETS = {
        "isic": ("ISIC Dermoscopy Dataset", "Dermoscopy"),
        "brats": ("BraTS Brain Tumor Segmentation Dataset", "MRI"),
        "chestx-ray": ("ChestX-ray8 / ChestX-ray14", "X-Ray"),
        "mimic": ("MIMIC Clinical Database", "EHR / Clinical"),
        "imagenet": ("ImageNet Benchmark", "Natural Images"),
        "cifar": ("CIFAR Benchmark Dataset", "Natural Images"),
        "adni": ("ADNI Alzheimer's Imaging Cohort", "PET / MRI"),
        "eyepacs": ("EyePACS Retinal Dataset", "Fundus Photography"),
    }

    KNOWN_TASKS = {
        "melanoma": ("Melanoma Skin Cancer Classification", "Dermatology"),
        "brain tumor": ("Brain Tumor Segmentation", "Neuro-Oncology"),
        "alzheimer": ("Alzheimer's Disease Detection", "Neurology"),
        "retinopathy": ("Diabetic Retinopathy Grading", "Ophthalmology"),
        "migraine": ("Migraine Detection & Biomarker Analysis", "Neurology"),
        "chest": ("Chest Pathology Detection", "Pulmonology"),
        "segmentation": ("Medical Image Segmentation", "Medical Imaging"),
        "classification": ("Medical Disease Classification", "Medical AI"),
    }

    KNOWN_LIMITATIONS = [
        "limited dataset size",
        "class imbalance",
        "lack of external validation",
        "high computational overhead",
        "black-box interpretability",
        "modal incompatibility",
    ]

    def extract_entities(self, title: str, abstract: str) -> Dict[str, Any]:
        text = f"{title} {abstract}".lower()

        methods: List[MethodEntity] = []
        for kw, (name, category) in self.KNOWN_METHODS.items():
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                methods.append(MethodEntity(name=name, category=category))

        datasets: List[DatasetEntity] = []
        for kw, (name, modality) in self.KNOWN_DATASETS.items():
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                datasets.append(DatasetEntity(name=name, modality=modality))

        tasks: List[TaskEntity] = []
        for kw, (name, domain) in self.KNOWN_TASKS.items():
            if re.search(r'\b' + re.escape(kw) + r'\b', text):
                tasks.append(TaskEntity(name=name, domain=domain))

        limitations: List[str] = []
        for lim in self.KNOWN_LIMITATIONS:
            if lim in text:
                limitations.append(lim.title())

        # Defaults if empty
        if not methods:
            methods.append(MethodEntity(name="Deep Neural Network", category="Deep Learning"))
        if not datasets:
            datasets.append(DatasetEntity(name="Clinical Imaging Benchmark", modality="Multi-modal"))
        if not tasks:
            tasks.append(TaskEntity(name="Medical Image Diagnosis", domain="Healthcare AI"))
        if not limitations:
            limitations.append("Requires broader clinical trial validation")

        return {
            "methods": methods,
            "datasets": datasets,
            "tasks": tasks,
            "limitations": limitations,
        }


entity_extractor = EntityExtractor()
