document.addEventListener("DOMContentLoaded", () =>{
    const fullNameFields = document.querySelectorAll('input[name="first_name"], input[name="last_name"]')
    const isOrgCheckbox = document.getElementById("is_org");
    const orgFields = document.getElementById("org-fields");
    const personalFields = document.getElementById("personal-fields");
    const orgNameField = document.querySelector('input[name="name"]');
    const optionalText = document.querySelector(".optional-text");
    const industryChoiceField = document.querySelector('select[name="industry_choice"]');
    const industryCustomField = document.querySelector('input[name="industry_custom"]');
    const industryChoiceLabel = document.querySelector(".industry_choice_label");
    const industryCustomLabel = document.querySelector(".industry_custom_label");
    const btnHideIndustryCustom = document.getElementById("btn-hide-industry-custom");

    if (isOrgCheckbox.checked) {
      optionalText.classList.add("hidden")
      orgNameField.required = true;
    }

    isOrgCheckbox.addEventListener("change", () => {
      if (isOrgCheckbox.checked) {
        orgFields.classList.remove("hidden");
        personalFields.classList.add("hidden");
        orgNameField.required = true;
        optionalText.classList.add("hidden");
        fullNameFields.forEach(field => {
          field.required = false;
        });
      } else {
        orgFields.classList.add("hidden");
        personalFields.classList.remove("hidden");
        orgNameField.required = false;
        optionalText.classList.remove("hidden");
        fullNameFields.forEach(field => {
          field.required = true;
        });
      }
    });

    if(industryChoiceField){
      industryChoiceField.addEventListener("change", function(){
        if(this.value === "other"){
          industryChoiceLabel.classList.add("hidden");
          industryCustomLabel.classList.remove("hidden");
          industryCustomField.setAttribute("required", true)
        }
      })
    }

    if (btnHideIndustryCustom) {
      btnHideIndustryCustom.onclick = () => {
        industryCustomField.setAttribute("required", false)
        industryChoiceLabel.classList.remove("hidden");
        industryCustomLabel.classList.add("hidden");
        industryChoiceField.selectedIndex = 0;
      };
    }
  })