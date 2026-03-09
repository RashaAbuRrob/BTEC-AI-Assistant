from config.settings import AIAssistantConfig

class AIAssistant:
    """BTEC Smart Assistant - مساعد BTEC الذكي"""
    
    def __init__(self):
        self.name = AIAssistantConfig.ASSISTANT_NAME
        self.name_en = AIAssistantConfig.ASSISTANT_NAME_EN
        self.model = AIAssistantConfig.MODEL
        self.temperature = AIAssistantConfig.TEMPERATURE
        self.api_key = AIAssistantConfig.OPENAI_API_KEY
        
    def generate_response(self, query, context=None):
        """Generate response about BTEC topics"""
        try:
            # Build context string from retrieved documents
            context_str = ""
            if context and len(context) > 0:
                context_str = "معلومات ذات صلة من قاعدة البيانات:\n"
                for doc in context:
                    context_str += f"- {doc['filename']}: {doc['preview']}\n"
            else:
                context_str = "لا توجد معلومات محددة في قاعدة البيانات"
            
            # Prepare the prompt - answer as a BTEC expert
            system_prompt = f"""أنت {self.name} ({self.name_en}).
            أنت مساعد ذكي متخصص في مؤهلات BTEC والتعليم.
            تجيب على جميع الأسئلة المتعلقة بـ BTEC بناءً على معرفتك الشاملة.
            إذا كان لديك معلومات من قاعدة البيانات، استخدمها.
            إذا لم تكن هناك معلومات محددة، استخدم معرفتك العامة عن BTEC."""
            
            user_message = f"""السياق والمعلومات:
{context_str}

السؤال: {query}

الرجاء تقديم إجابة شاملة ومفيدة عن BTEC."""
            
            # Call OpenAI or mock response
            response = self._generate_mock_response(query, context)
            
            return response
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
    
    def _clean_text(self, text):
        """Clean PDF extracted text by removing excessive dots and formatting artifacts"""
        # Remove excessive dots
        text = text.replace('............', ' ')
        text = text.replace('...........', ' ')
        text = text.replace('..........', ' ')
        text = text.replace('.........', ' ')
        text = text.replace('........', ' ')
        text = text.replace('.......', ' ')
        text = text.replace('......', ' ')
        text = text.replace('.....', ' ')
        text = text.replace('....', ' ')
        text = text.replace('...', '.')
        text = text.replace('..', '.')
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _generate_mock_response(self, query, context=None):
        """Generate response based on available context from BTEC database"""
        query_lower = query.lower()
        
        # Define comprehensive keyword-to-response mapping
        keyword_responses = [
            (['ما هو', 'what is', 'define', 'تعريف'], 'BTEC هو اختصار لـ Business and Technology Education Council. وهي مؤهلات معترف بها دولياً تقدم تعليماً عملياً وذا صلة بعالم العمل. تركز BTEC على المهارات العملية والخبرة في العالم الحقيقي بدلاً من الامتحانات النظرية فقط.'),
            (['مؤهلات', 'qualifications', 'certificate'], 'مؤهلات BTEC تشمل: BTEC Level 1 التمهيدي، BTEC Level 2 First، BTEC Level 3 National، BTEC Higher National Diploma (HND)، و BTEC Higher National Certificate (HNC). كل مستوى يوفر مهارات وعلومات متزايدة التعقيد.'),
            (['مستوى', 'level', 'levels'], 'توجد عدة مستويات من BTEC: المستوى 1 للمبتدئين، المستوى 2 للطلاب الأصغر سناً، المستوى 3 للطلاب الأكبر سناً، وشهادات دبلوم وشهادات BTEC العليا للتعليم ما بعد المدرسة.'),
            (['فوائد', 'benefits', 'advantage'], 'فوائد BTEC تشمل: تعلم عملي وتجربة في العالم الحقيقي، معترف به من قبل أصحاب العمل عالمياً، مسارات تقدم مرنة، تطوير مهارات قابلة للتطبيق، وفرص العمل في المشاريع.'),
            (['مواضيع', 'تخصصات', 'subjects', 'topics'], 'تغطي BTEC موضوعات عديدة منها: الأعمال والتجارة، الهندسة، الصحة والرعاية الاجتماعية، تكنولوجيا المعلومات، الضيافة والسياحة، والفنون والتصميم.'),
            (['متطلبات', 'requirements', 'شروط', 'conditions'], 'متطلبات الالتحاق ببرنامج BTEC تختلف حسب المستوى والتخصص، لكن بشكل عام تحتاج إلى جودة عالية في الرياضيات والإنجليزية، والالتزام بالدراسة العملية والمشاريع.'),
            (['مدة', 'duration', 'كم سنة', 'how long'], 'برامج BTEC متنوعة المدد والمسارات الوظيفية. BTEC Level 1 و 2 عادة ما تكون سنة واحدة، و Level 3 تكون حول سنتين. الخريجون يعملون في قطاعات متعددة بما فيها الأعمال والهندسة والصحة.'),
            (['من', 'who', 'طور', 'developed', 'أسس', 'founder'], 'BTEC تم تطويرها بواسطة Pearson (والمعروفة سابقاً باسم EDEXCEL)، وهي شركة عالمية متخصصة في التعليم والمؤهلات. تابعت BTEC معايير عالية من الجودة والاعتراف الدولي، وتُقدم الآن في أكثر من 100 دولة حول العالم.'),
        ]
        
        # Try to match keywords in the query
        for keywords_list, response in keyword_responses:
            for keyword in keywords_list:
                if keyword in query_lower:
                    return response
        
        # If we have context from the database, use it for generic questions
        if context and len(context) > 0:
            best_doc = context[0]
            if 'preview' in best_doc:
                preview_text = self._clean_text(best_doc['preview'])
                
                # Extract meaningful content
                lines = preview_text.split('.')
                meaningful_lines = [line.strip() for line in lines if line.strip() and len(line.strip()) > 15]
                
                if meaningful_lines:
                    response = f"✓ معلومات من قاعدة البيانات:\n\n"
                    response += "\n".join([f"• {line}" for line in meaningful_lines[:3]])
                    response += f"\n\n💡 السؤال: {query}"
                    response += "\n\nللمزيد من التفاصيل، يمكنك السؤال عن مستويات BTEC أو التخصصات أو المتطلبات."
                    return response
        
        # Default response for questions we don't have specific answers for
        return f"سؤال مهم عن BTEC: '{query}'\n\n📚 للحصول على إجابة أفضل، يمكنك السؤال عن:\n• ما هو برنامج BTEC؟\n• مستويات ومؤهلات BTEC\n• التخصصات والمواضيع المتاحة\n• متطلبات الالتحاق\n• مدة البرنامج\n• فوائد البرنامج"
    
    def generate_with_openai(self, query, context):
        """Generate response using OpenAI API"""
        try:
            import openai
            openai.api_key = self.api_key
            
            context_str = ""
            if context:
                context_str = "Relevant documents:\n"
                for doc in context:
                    context_str += f"- {doc['filename']}: {doc['preview']}\n"
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are {self.name}, a helpful BTEC assistant."
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context_str}\n\nQuestion: {query}"
                    }
                ],
                temperature=self.temperature,
                max_tokens=AIAssistantConfig.MAX_TOKENS
            )
            
            return response['choices'][0]['message']['content']
        except Exception as e:
            raise Exception(f"Error with OpenAI API: {str(e)}")
