"""
Internationalization (i18n) module for UI translations.

This module provides translations for the user interface in multiple languages,
allowing users to interact with the application in their preferred language
while generating content in any language they choose.
"""

from typing import Dict, Any


# ============================================================================
# TRANSLATIONS DICTIONARY
# ============================================================================

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # ========================================================================
    # ENGLISH TRANSLATIONS
    # ========================================================================
    "English": {
        # Page header
        "page_title": "AI Content Generator",
        "page_subtitle": "Generate high-quality blog posts using AI. Configure your content parameters in the sidebar and click generate.",
        
        # Main tabs
        "tab_blog": "📝 Blog Content",
        "tab_social": "📣 Social Media",
        
        # Sidebar sections
        "sidebar_title": "🎯 Content Configuration",
        "sidebar_subtitle": "Configure the parameters for your blog post generation.",
        "ui_language_label": "🌐 Interface Language",
        "ui_language_help": "Select your preferred language for the interface",
        
        # Topic section
        "topic_header": "📝 Topic",
        "topic_label": "Blog Topic",
        "topic_placeholder": "e.g., The Future of Artificial Intelligence",
        "topic_help": "Enter the main subject or theme for your blog post",
        
        # Audience section
        "audience_header": "👥 Target Audience",
        "audience_label": "Target Audience",
        "audience_placeholder": "e.g., software developers, general public",
        "audience_help": "Specify who will be reading this content",
        
        # Style section
        "style_header": "🎨 Writing Style",
        "tone_label": "Tone",
        "tone_help": "Choose the writing tone that best fits your audience and purpose",
        "tone_professional": "Formal, business-appropriate language",
        "tone_casual": "Relaxed, conversational style",
        "tone_friendly": "Warm, approachable, and personable",
        "tone_technical": "Detailed, precise, with technical terminology",
        
        # Language section
        "language_header": "🌍 Language",
        "content_language_label": "Content Language",
        "content_language_help": "Select the language for content generation",
        
        # Language options translations
        "lang_english": "English",
        "lang_spanish": "Spanish",
        "lang_french": "French",
        "lang_italian": "Italian",
        
        # Content Writing Style section
        "style_selector_header": "Content Writing Style",
        "style_selector_label": "Select Style",
        "style_selector_help": "Choose how the content should be written (tone, structure, vocabulary)",
        "style_default": "Default",
        "style_seo": "SEO Optimized",
        "style_divulgative": "Educational/Divulgative",
        "style_kids": "Kid-Friendly",
        "style_default_desc": "Standard writing without special constraints",
        "style_seo_desc": "Optimized for search engines with clear structure and keyword focus",
        "style_divulgative_desc": "Clear explanations, accessible language, educational approach",
        "style_kids_desc": "Simple language for children ages 6-10",
        
        # LLM Provider section
        "provider_header": "🤖 LLM Provider",
        "provider_label": "Select Provider",
        "provider_help": "Choose between cloud (Groq) or local (Ollama) LLM",
        "provider_groq": "Groq (Cloud)",
        "provider_ollama": "Ollama (Local)",
        
        # Generate section
        "generate_header": "🚀 Generate",
        "generate_note": "⚠️ Make sure to fill in the topic and audience fields",
        "generate_button": "Generate Blog Post",
        "generating_spinner": "🤖 Generating your blog post... This may take a few moments.",
        
        # Social media UI
        "social_title": "📣 Social Media Posts",
        "social_subtitle": "Transform your blog content into platform-optimized social posts.",
        "social_no_content": "No blog content available yet.",
        "social_instruction_1": "1. Switch to the **Blog Content** tab",
        "social_instruction_2": "2. Generate a blog post first",
        "social_instruction_3": "3. Return here to create social media posts",
        "social_platform_label": "Select Platform",
        "social_generate_button": "✨ Generate {platform} Post",
        "social_generating": "Generating {platform} post...",
        
        # Footer
        "footer_tip": "💡 **Tip:** Be specific with your topic and audience for better results!",
        
        # Validation messages
        "validation_topic": "⚠️ Please enter a topic for your blog post.",
        "validation_audience": "⚠️ Please specify your target audience.",
        
        # Output messages
        "output_header": "✅ Generated Blog Post",
        "output_description": "Your blog post has been generated successfully. You can read it below or copy it for use.",
        "output_label": "Generated Content",
        "output_copy_hint": "📋 Use the text area controls to copy",
        "output_stats": "📊 {words} words · {chars} characters",
        "success_message": "✅ Blog post generated successfully!",
        "previous_content_info": "ℹ️ Showing previously generated content. Modify inputs and click Generate to create new content.",
        
        # Error messages
        "ollama_error": "⚠️ Ollama is not available. Please make sure Ollama is running.",
        "ollama_help": "💡 To use Ollama: 1) Install from https://ollama.ai 2) Run 'ollama serve' 3) Pull a model with 'ollama pull llama3.2'",
        
        # Empty state
        "empty_welcome": "### 🚀 Welcome to AI Content Generator!",
        "empty_instructions": "To get started:",
        "empty_step1": "1. Fill in the **Topic** and **Target Audience** in the sidebar",
        "empty_step2": "2. Select your preferred **Tone** and **Language**",
        "empty_step3": "3. Click the **Generate Blog Post** button",
        "empty_tip": "💡 **Tip:** The more specific you are with your inputs, the better the generated content will be!",
        
        # Error messages
        "error_title": "❌ Content Generation Failed",
        "error_description": "An error occurred while generating your blog post:",
        "error_suggestions_title": "**Suggestions:**",
        "error_suggestion1": "- Check your internet connection",
        "error_suggestion2": "- Verify your API key is correctly set in the `.env` file",
        "error_suggestion3": "- Try again with different parameters",
        "config_error": "⚠️ Configuration Error: {error}",
        
        # Identity Profile
        "identity_role_ceo": "CEO / Founder",
        "identity_role_marketing": "Marketing Manager",
        "identity_role_engineer": "Software Engineer",
        "identity_role_scientist": "Data Scientist",
        "identity_role_product": "Product Manager",
        "identity_role_designer": "Designer",
        "identity_role_writer": "Writer / Author",
        "identity_industry_tech": "Technology / SaaS",
        "identity_industry_fintech": "FinTech / Finance",
        "identity_industry_health": "Healthcare / MedTech",
        "identity_industry_ecommerce": "E-commerce / Retail",
        "identity_industry_marketing": "Marketing / Advertising",
        "identity_industry_consulting": "Consulting Services",
        "identity_industry_education": "Education / EdTech",
        "identity_tone_formal": "Professional and formal",
        "identity_tone_approachable": "Professional yet approachable",
        "identity_tone_conversational": "Friendly and conversational",
        "identity_tone_technical": "Technical and precise",
        "identity_tone_inspiring": "Inspiring and motivational",
        "identity_tone_empathetic": "Warm and empathetic",
        "identity_tone_innovative": "Bold and innovative",
        "identity_values_innovation": "Innovation, transparency, integrity",
        "identity_values_customer": "Customer success, quality, reliability",
        "identity_values_sustainability": "Sustainability, ethics, social impact",
        "identity_values_excellence": "Excellence, collaboration, growth",
        "identity_values_creativity": "Creativity, passion, authenticity",
        "identity_values_trust": "Trust, security, privacy",
        "identity_values_diversity": "Diversity, inclusion, equity",
        "identity_custom": "Custom (write your own)...",
        "identity_select_placeholder": "Select or type custom...",
        "identity_header": "Identity Profile (Optional)",
        "identity_enable": "Enable identity personalization",
        "identity_enable_help": "Add identity information to personalize all generated content",
        "identity_type_label": "Type",
        "identity_type_help": "Select whether this is a person or company identity",
        "identity_type_person": "Person",
        "identity_type_company": "Company",
        "identity_name_label": "Name",
        "identity_name_placeholder": "e.g., Dr. Sarah Johnson or TechCorp Inc.",
        "identity_name_help": "Full name of the person or company",
        "identity_role_label": "Role",
        "identity_industry_label": "Industry",
        "identity_role_placeholder_person": "e.g., Senior AI Researcher",
        "identity_role_placeholder_company": "e.g., Technology / SaaS",
        "identity_role_help_person": "Your job title or professional role",
        "identity_role_help_company": "Your company industry or sector",
        "identity_role_suggestions": "Role Suggestions (click to see)",
        "identity_industry_suggestions": "Industry Suggestions (click to see)",
        "identity_background_label": "Background",
        "identity_about_label": "About",
        "identity_background_placeholder": "Describe your expertise, experience, and key qualifications...",
        "identity_about_placeholder": "Describe company mission, products, and value proposition...",
        "identity_background_help": "Brief description that will influence content generation",
        "identity_tone_label": "Tone of Voice (Optional)",
        "identity_tone_help": "How you want your content to sound",
        "identity_tone_custom_label": "Custom Tone",
        "identity_tone_custom_placeholder": "Or type your own tone",
        "identity_values_label": "Core Values (Optional)",
        "identity_values_help": "Key values to reflect in your content",
        "identity_values_custom_label": "Custom Values",
        "identity_values_custom_placeholder": "Or type your own values",
    },
    
    # ========================================================================
    # SPANISH TRANSLATIONS
    # ========================================================================
    "Español": {
        # Page header
        "page_title": "Generador de Contenido IA",
        "page_subtitle": "Genera artículos de blog de alta calidad usando IA. Configura los parámetros de tu contenido en la barra lateral y haz clic en generar.",
        
        # Sidebar sections
        "sidebar_title": "🎯 Configuración de Contenido",
        "sidebar_subtitle": "Configura los parámetros para generar tu artículo de blog.",
        "ui_language_label": "🌐 Idioma de la Interfaz",
        "ui_language_help": "Selecciona tu idioma preferido para la interfaz",
        
        # Topic section
        "topic_header": "📝 Tema",
        "topic_label": "Tema del Blog",
        "topic_placeholder": "ej., El Futuro de la Inteligencia Artificial",
        "topic_help": "Introduce el tema o asunto principal para tu artículo",
        
        # Audience section
        "audience_header": "👥 Audiencia Objetivo",
        "audience_label": "Audiencia Objetivo",
        "audience_placeholder": "ej., desarrolladores de software, público general",
        "audience_help": "Especifica quién leerá este contenido",
        
        # Style section
        "style_header": "🎨 Estilo de Escritura",
        "tone_label": "Tono",
        "tone_help": "Elige el tono de escritura que mejor se adapte a tu audiencia y propósito",
        "tone_professional": "Lenguaje formal, apropiado para negocios",
        "tone_casual": "Estilo relajado y conversacional",
        "tone_friendly": "Cálido, cercano y personal",
        "tone_technical": "Detallado, preciso, con terminología técnica",
        
        # Language section
        "language_header": "🌍 Idioma",
        "content_language_label": "Idioma del Contenido",
        "content_language_help": "Selecciona el idioma para generar el contenido",
        
        # Language options translations
        "lang_english": "Inglés",
        "lang_spanish": "Español",
        "lang_french": "Francés",
        "lang_italian": "Italiano",
        
        # Content Writing Style section
        "style_selector_header": "Estilo de Escritura del Contenido",
        "style_selector_label": "Seleccionar Estilo",
        "style_selector_help": "Elige cómo debe escribirse el contenido (tono, estructura, vocabulario)",
        "style_default": "Por Defecto",
        "style_seo": "Optimizado para SEO",
        "style_divulgative": "Educativo/Divulgativo",
        "style_kids": "Para Niños",
        "style_default_desc": "Escritura estándar sin restricciones especiales",
        "style_seo_desc": "Optimizado para motores de búsqueda con estructura clara y enfoque en palabras clave",
        "style_divulgative_desc": "Explicaciones claras, lenguaje accesible, enfoque educativo",
        "style_kids_desc": "Lenguaje simple para niños de 6-10 años",
        
        # LLM Provider section
        "provider_header": "🤖 Proveedor LLM",
        "provider_label": "Seleccionar Proveedor",
        "provider_help": "Elige entre nube (Groq) o local (Ollama)",
        "provider_groq": "Groq (Nube)",
        "provider_ollama": "Ollama (Local)",
        
        # Generate section
        "generate_header": "🚀 Generar",
        "generate_note": "⚠️ Asegúrate de completar los campos de tema y audiencia",
        "generate_button": "Generar Artículo de Blog",
        "generating_spinner": "🤖 Generando tu publicación... Esto puede tomar unos momentos.",
        
        # Social media UI
        "social_title": "📣 Posts para Redes Sociales",
        "social_subtitle": "Transforma tu contenido del blog en posts optimizados para cada plataforma.",
        "social_no_content": "Aún no hay contenido de blog disponible.",
        "social_instruction_1": "1. Cambia a la pestaña **Contenido del Blog**",
        "social_instruction_2": "2. Genera primero un artículo de blog",
        "social_instruction_3": "3. Regresa aquí para crear posts de redes sociales",
        "social_platform_label": "Seleccionar Plataforma",
        "social_generate_button": "✨ Generar Post para {platform}",
        "social_generating": "Generando post para {platform}...",
        
        # Footer
        "footer_tip": "💡 **Consejo:** ¡Sé específico con tu tema y audiencia para mejores resultados!",
        
        # Validation messages
        "validation_topic": "⚠️ Por favor, introduce un tema para tu artículo de blog.",
        "validation_audience": "⚠️ Por favor, especifica tu audiencia objetivo.",
        
        # Output messages
        "output_header": "✅ Artículo de Blog Generado",
        "output_description": "Tu artículo de blog se ha generado exitosamente. Puedes leerlo a continuación o copiarlo para usarlo.",
        "output_label": "Contenido Generado",
        "output_copy_hint": "📋 Usa los controles del área de texto para copiar",
        "output_stats": "📊 {words} palabras · {chars} caracteres",
        "success_message": "✅ ¡Artículo de blog generado exitosamente!",
        "previous_content_info": "ℹ️ Mostrando contenido generado previamente. Modifica los parámetros y haz clic en Generar para crear contenido nuevo.",
        
        # Error messages
        "ollama_error": "⚠️ Ollama no está disponible. Asegúrate de que Ollama esté ejecutándose.",
        "ollama_help": "💡 Para usar Ollama: 1) Instalar desde https://ollama.ai 2) Ejecutar 'ollama serve' 3) Descargar un modelo con 'ollama pull llama3.2'",
        
        # Empty state
        "empty_welcome": "### 🚀 ¡Bienvenido al Generador de Contenido IA!",
        "empty_instructions": "Para comenzar:",
        "empty_step1": "1. Completa el **Tema** y la **Audiencia Objetivo** en la barra lateral",
        "empty_step2": "2. Selecciona tu **Tono** e **Idioma** preferidos",
        "empty_step3": "3. Haz clic en el botón **Generar Artículo de Blog**",
        "empty_tip": "💡 **Consejo:** ¡Cuanto más específico seas con tus parámetros, mejor será el contenido generado!",
        
        # Error messages
        "error_title": "❌ Error en la Generación de Contenido",
        "error_description": "Ocurrió un error al generar tu artículo de blog:",
        "error_suggestions_title": "**Sugerencias:**",
        "error_suggestion1": "- Verifica tu conexión a internet",
        "error_suggestion2": "- Comprueba que tu clave API esté correctamente configurada en el archivo `.env`",
        "error_suggestion3": "- Intenta nuevamente con parámetros diferentes",
        "config_error": "⚠️ Error de Configuración: {error}",
        
        # Identity Profile
        "identity_role_ceo": "CEO / Fundador",
        "identity_role_marketing": "Gerente de Marketing",
        "identity_role_engineer": "Ingeniero de Software",
        "identity_role_scientist": "Científico de Datos",
        "identity_role_product": "Gerente de Producto",
        "identity_role_designer": "Diseñador",
        "identity_role_writer": "Escritor / Autor",
        "identity_industry_tech": "Tecnología / SaaS",
        "identity_industry_fintech": "FinTech / Finanzas",
        "identity_industry_health": "Salud / MedTech",
        "identity_industry_ecommerce": "Comercio electrónico / Retail",
        "identity_industry_marketing": "Marketing / Publicidad",
        "identity_industry_consulting": "Servicios de Consultoría",
        "identity_industry_education": "Educación / EdTech",
        "identity_tone_formal": "Profesional y formal",
        "identity_tone_approachable": "Profesional pero cercano",
        "identity_tone_conversational": "Amigable y conversacional",
        "identity_tone_technical": "Técnico y preciso",
        "identity_tone_inspiring": "Inspirador y motivacional",
        "identity_tone_empathetic": "Cálido y empático",
        "identity_tone_innovative": "Audaz e innovador",
        "identity_values_innovation": "Innovación, transparencia, integridad",
        "identity_values_customer": "Éxito del cliente, calidad, confiabilidad",
        "identity_values_sustainability": "Sostenibilidad, ética, impacto social",
        "identity_values_excellence": "Excelencia, colaboración, crecimiento",
        "identity_values_creativity": "Creatividad, pasión, autenticidad",
        "identity_values_trust": "Confianza, seguridad, privacidad",
        "identity_values_diversity": "Diversidad, inclusión, equidad",
        "identity_custom": "Personalizado (escribe el tuyo)...",
        "identity_select_placeholder": "Selecciona o escribe...",
        "identity_header": "Perfil de Identidad (Opcional)",
        "identity_enable": "Activar personalización de identidad",
        "identity_enable_help": "Agrega información de identidad para personalizar todo el contenido generado",
        "identity_type_label": "Tipo",
        "identity_type_help": "Selecciona si es una identidad personal o empresarial",
        "identity_type_person": "Persona",
        "identity_type_company": "Empresa",
        "identity_name_label": "Nombre",
        "identity_name_placeholder": "ej., Dr. Sarah Johnson o TechCorp Inc.",
        "identity_name_help": "Nombre completo de la persona o empresa",
        "identity_role_label": "Rol",
        "identity_industry_label": "Industria",
        "identity_role_placeholder_person": "ej., Investigador Senior de IA",
        "identity_role_placeholder_company": "ej., Tecnología / SaaS",
        "identity_role_help_person": "Tu título o rol profesional",
        "identity_role_help_company": "Industria o sector de tu empresa",
        "identity_role_suggestions": "Sugerencias de Rol (clic para ver)",
        "identity_industry_suggestions": "Sugerencias de Industria (clic para ver)",
        "identity_background_label": "Experiencia",
        "identity_about_label": "Acerca de",
        "identity_background_placeholder": "Describe tu experiencia, conocimientos y cualificaciones clave...",
        "identity_about_placeholder": "Describe la misión, productos y propuesta de valor de la empresa...",
        "identity_background_help": "Breve descripción que influirá en la generación de contenido",
        "identity_tone_label": "Tono de Voz (Opcional)",
        "identity_tone_help": "Cómo quieres que suene tu contenido",
        "identity_tone_custom_label": "Tono Personalizado",
        "identity_tone_custom_placeholder": "O escribe tu propio tono",
        "identity_values_label": "Valores Fundamentales (Opcional)",
        "identity_values_help": "Valores clave a reflejar en tu contenido",
        "identity_values_custom_label": "Valores Personalizados",
        "identity_values_custom_placeholder": "O escribe tus propios valores",
    },
    
    # ========================================================================
    # FRENCH TRANSLATIONS
    # ========================================================================
    "Français": {
        # Page header
        "page_title": "Générateur de Contenu IA",
        "page_subtitle": "Générez des articles de blog de haute qualité avec l'IA. Configurez vos paramètres de contenu dans la barre latérale et cliquez sur générer.",
        
        # Sidebar sections
        "sidebar_title": "🎯 Configuration du Contenu",
        "sidebar_subtitle": "Configurez les paramètres pour générer votre article de blog.",
        "ui_language_label": "🌐 Langue de l'Interface",
        "ui_language_help": "Sélectionnez votre langue préférée pour l'interface",
        
        # Topic section
        "topic_header": "📝 Sujet",
        "topic_label": "Sujet du Blog",
        "topic_placeholder": "ex., L'Avenir de l'Intelligence Artificielle",
        "topic_help": "Entrez le sujet ou le thème principal de votre article",
        
        # Audience section
        "audience_header": "👥 Public Cible",
        "audience_label": "Public Cible",
        "audience_placeholder": "ex., développeurs de logiciels, grand public",
        "audience_help": "Spécifiez qui lira ce contenu",
        
        # Style section
        "style_header": "🎨 Style d'Écriture",
        "tone_label": "Ton",
        "tone_help": "Choisissez le ton d'écriture qui convient le mieux à votre public et à votre objectif",
        "tone_professional": "Langage formel, approprié aux affaires",
        "tone_casual": "Style décontracté et conversationnel",
        "tone_friendly": "Chaleureux, accessible et personnel",
        "tone_technical": "Détaillé, précis, avec terminologie technique",
        
        # Language section
        "language_header": "🌍 Langue",
        "content_language_label": "Langue du Contenu",
        "content_language_help": "Sélectionnez la langue pour la génération du contenu",        
        # Language options translations
        "lang_english": "Anglais",
        "lang_spanish": "Espagnol",
        "lang_french": "Français",
        "lang_italian": "Italien",
        
        # Content Writing Style section
        "style_selector_header": "Style d'Écriture du Contenu",
        "style_selector_label": "Sélectionner le Style",
        "style_selector_help": "Choisissez comment le contenu doit être écrit (ton, structure, vocabulaire)",
        "style_default": "Par Défaut",
        "style_seo": "Optimisé SEO",
        "style_divulgative": "Éducatif/Vulgarisation",
        "style_kids": "Pour Enfants",
        "style_default_desc": "Écriture standard sans contraintes spéciales",
        "style_seo_desc": "Optimisé pour les moteurs de recherche avec structure claire et focus sur les mots-clés",
        "style_divulgative_desc": "Explications claires, langage accessible, approche éducative",
        "style_kids_desc": "Langage simple pour enfants de 6-10 ans",
        
        # LLM Provider section
        "provider_header": "🤖 Fournisseur LLM",
        "provider_label": "Sélectionner le Fournisseur",
        "provider_help": "Choisissez entre cloud (Groq) ou local (Ollama)",
        "provider_groq": "Groq (Cloud)",
        "provider_ollama": "Ollama (Local)",
        
        # Generate section
        "generate_header": "🚀 Générer",
        "generate_note": "⚠️ Assurez-vous de remplir les champs sujet et public",
        "generate_button": "Générer l'Article de Blog",
        "generating_spinner": "🤖 Génération de votre article... Cela peut prendre quelques instants.",
        
        # Footer
        "footer_tip": "💡 **Astuce:** Soyez précis avec votre sujet et votre public pour de meilleurs résultats!",
        
        # Validation messages
        "validation_topic": "⚠️ Veuillez entrer un sujet pour votre article de blog.",
        "validation_audience": "⚠️ Veuillez spécifier votre public cible.",
        
        # Output messages
        "output_header": "✅ Article de Blog Généré",
        "output_description": "Votre article de blog a été généré avec succès. Vous pouvez le lire ci-dessous ou le copier pour l'utiliser.",
        "output_label": "Contenu Généré",
        "output_copy_hint": "📋 Utilisez les contrôles de la zone de texte pour copier",
        "output_stats": "📊 {words} mots · {chars} caractères",
        "success_message": "✅ Article de blog généré avec succès!",
        "previous_content_info": "ℹ️ Affichage du contenu précédemment généré. Modifiez les paramètres et cliquez sur Générer pour créer un nouveau contenu.",
        
        # Error messages
        "ollama_error": "⚠️ Ollama n'est pas disponible. Assurez-vous qu'Ollama est en cours d'exécution.",
        "ollama_help": "💡 Pour utiliser Ollama: 1) Installer depuis https://ollama.ai 2) Exécuter 'ollama serve' 3) Télécharger un modèle avec 'ollama pull llama3.2'",
        
        # Empty state
        "empty_welcome": "### 🚀 Bienvenue au Générateur de Contenu IA!",
        "empty_instructions": "Pour commencer:",
        "empty_step1": "1. Remplissez le **Sujet** et le **Public Cible** dans la barre latérale",
        "empty_step2": "2. Sélectionnez votre **Ton** et **Langue** préférés",
        "empty_step3": "3. Cliquez sur le bouton **Générer l'Article de Blog**",
        "empty_tip": "💡 **Astuce:** Plus vous êtes précis avec vos paramètres, meilleur sera le contenu généré!",
        
        # Error messages
        "error_title": "❌ Échec de la Génération de Contenu",
        "error_description": "Une erreur s'est produite lors de la génération de votre article de blog:",
        "error_suggestions_title": "**Suggestions:**",
        "error_suggestion1": "- Vérifiez votre connexion Internet",
        "error_suggestion2": "- Vérifiez que votre clé API est correctement définie dans le fichier `.env`",
        "error_suggestion3": "- Réessayez avec des paramètres différents",
        "config_error": "⚠️ Erreur de Configuration: {error}",
    },
    
    # ========================================================================
    # ITALIAN TRANSLATIONS
    # ========================================================================
    "Italiano": {
        # Page header
        "page_title": "Generatore di Contenuti IA",
        "page_subtitle": "Genera articoli di blog di alta qualità usando l'IA. Configura i parametri del tuo contenuto nella barra laterale e fai clic su genera.",
        
        # Sidebar sections
        "sidebar_title": "🎯 Configurazione Contenuto",
        "sidebar_subtitle": "Configura i parametri per generare il tuo articolo di blog.",
        "ui_language_label": "🌐 Lingua dell'Interfaccia",
        "ui_language_help": "Seleziona la tua lingua preferita per l'interfaccia",
        
        # Topic section
        "topic_header": "📝 Argomento",
        "topic_label": "Argomento del Blog",
        "topic_placeholder": "es., Il Futuro dell'Intelligenza Artificiale",
        "topic_help": "Inserisci l'argomento o il tema principale per il tuo articolo",
        
        # Audience section
        "audience_header": "👥 Pubblico di Destinazione",
        "audience_label": "Pubblico di Destinazione",
        "audience_placeholder": "es., sviluppatori di software, pubblico generale",
        "audience_help": "Specifica chi leggerà questo contenuto",
        
        # Style section
        "style_header": "🎨 Stile di Scrittura",
        "tone_label": "Tono",
        "tone_help": "Scegli il tono di scrittura che si adatta meglio al tuo pubblico e al tuo scopo",
        "tone_professional": "Linguaggio formale, appropriato per affari",
        "tone_casual": "Stile rilassato e conversazionale",
        "tone_friendly": "Caldo, accessibile e personale",
        "tone_technical": "Dettagliato, preciso, con terminologia tecnica",
        
        # Language section
        "language_header": "🌍 Lingua",
        "content_language_label": "Lingua del Contenuto",
        "content_language_help": "Seleziona la lingua per la generazione del contenuto",        
        # Language options translations
        "lang_english": "Inglese",
        "lang_spanish": "Spagnolo",
        "lang_french": "Francese",
        "lang_italian": "Italiano",
        
        # Content Writing Style section
        "style_selector_header": "Stile di Scrittura del Contenuto",
        "style_selector_label": "Seleziona Stile",
        "style_selector_help": "Scegli come deve essere scritto il contenuto (tono, struttura, vocabolario)",
        "style_default": "Predefinito",
        "style_seo": "Ottimizzato SEO",
        "style_divulgative": "Educativo/Divulgativo",
        "style_kids": "Per Bambini",
        "style_default_desc": "Scrittura standard senza vincoli speciali",
        "style_seo_desc": "Ottimizzato per i motori di ricerca con struttura chiara e focus sulle parole chiave",
        "style_divulgative_desc": "Spiegazioni chiare, linguaggio accessibile, approccio educativo",
        "style_kids_desc": "Linguaggio semplice per bambini dai 6 ai 10 anni",
        
        # LLM Provider section
        "provider_header": "🤖 Provider LLM",
        "provider_label": "Seleziona Provider",
        "provider_help": "Scegli tra cloud (Groq) o locale (Ollama)",
        "provider_groq": "Groq (Cloud)",
        "provider_ollama": "Ollama (Locale)",
        
        # Generate section
        "generate_header": "🚀 Genera",
        "generate_note": "⚠️ Assicurati di compilare i campi argomento e pubblico",
        "generate_button": "Genera Articolo di Blog",        "generating_spinner": "🤖 Generazione del tuo post... Potrebbe richiedere qualche istante.",        
        # Footer
        "footer_tip": "💡 **Suggerimento:** Sii specifico con il tuo argomento e pubblico per risultati migliori!",
        
        # Validation messages
        "validation_topic": "⚠️ Per favore, inserisci un argomento per il tuo articolo di blog.",
        "validation_audience": "⚠️ Per favore, specifica il tuo pubblico di destinazione.",
        
        # Output messages
        "output_header": "✅ Articolo di Blog Generato",
        "output_description": "Il tuo articolo di blog è stato generato con successo. Puoi leggerlo qui sotto o copiarlo per usarlo.",
        "output_label": "Contenuto Generato",
        "output_copy_hint": "📋 Usa i controlli dell'area di testo per copiare",
        "output_stats": "📊 {words} parole · {chars} caratteri",
        "success_message": "✅ Articolo di blog generato con successo!",
        "previous_content_info": "ℹ️ Visualizzazione del contenuto generato precedentemente. Modifica i parametri e fai clic su Genera per creare nuovo contenuto.",
        
        # Error messages
        "ollama_error": "⚠️ Ollama non è disponibile. Assicurati che Ollama sia in esecuzione.",
        "ollama_help": "💡 Per usare Ollama: 1) Installa da https://ollama.ai 2) Esegui 'ollama serve' 3) Scarica un modello con 'ollama pull llama3.2'",
        
        # Empty state
        "empty_welcome": "### 🚀 Benvenuto al Generatore di Contenuti IA!",
        "empty_instructions": "Per iniziare:",
        "empty_step1": "1. Compila l'**Argomento** e il **Pubblico di Destinazione** nella barra laterale",
        "empty_step2": "2. Seleziona il tuo **Tono** e **Lingua** preferiti",
        "empty_step3": "3. Fai clic sul pulsante **Genera Articolo di Blog**",
        "empty_tip": "💡 **Suggerimento:** Più sei specifico con i tuoi parametri, migliore sarà il contenuto generato!",
        
        # Error messages
        "error_title": "❌ Generazione Contenuto Fallita",
        "error_description": "Si è verificato un errore durante la generazione del tuo articolo di blog:",
        "error_suggestions_title": "**Suggerimenti:**",
        "error_suggestion1": "- Controlla la tua connessione Internet",
        "error_suggestion2": "- Verifica che la tua chiave API sia correttamente impostata nel file `.env`",
        "error_suggestion3": "- Riprova con parametri diversi",
        "config_error": "⚠️ Errore di Configurazione: {error}",
    },
}


# ============================================================================
# TRANSLATION FUNCTIONS
# ============================================================================

def get_text(key: str, language: str = "English", **kwargs: Any) -> str:
    """
    Get translated text for a given key in the specified language.
    
    This function retrieves the appropriate translation for a text key
    based on the selected UI language. It supports formatting with kwargs.
    
    Args:
        key (str): The translation key to look up.
        language (str): The target language for translation. Default is "English".
        **kwargs: Optional formatting arguments for string interpolation.
    
    Returns:
        str: The translated text, or the key itself if translation is not found.
    
    Example:
        >>> get_text("page_title", "Español")
        'Generador de Contenido IA'
        >>> get_text("output_stats", "English", words=250, chars=1500)
        '📊 250 words · 1500 characters'
    """
    # Get the translation dictionary for the specified language
    translations = TRANSLATIONS.get(language, TRANSLATIONS["English"])
    
    # Get the translated text, fallback to English if not found
    text = translations.get(key, TRANSLATIONS["English"].get(key, key))
    
    # Format the text with any provided kwargs
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError):
            pass  # If formatting fails, return unformatted text
    
    return text


def get_available_languages() -> list[str]:
    """
    Get a list of all available UI languages.
    
    Returns:
        list: List of available language names.
    
    Example:
        >>> get_available_languages()
        ['English', 'Español', 'Français', 'Italiano']
    """
    return list(TRANSLATIONS.keys())
