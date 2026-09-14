document.addEventListener("DOMContentLoaded", function () {


    // =========================================================
    // COMMON MODAL FUNCTION
    // =========================================================

    function openModal(modal) {

        if (!modal) {
            return;
        }

        modal.classList.add("show");
        document.body.classList.add("modal-open");
    }


    function closeModal(modal) {

        if (!modal) {
            return;
        }

        modal.classList.remove("show");
        document.body.classList.remove("modal-open");
    }


    // =========================================================
    // CUSTOMER PROFILE
    // =========================================================

    const customerProfileButton =
        document.getElementById("customerProfileButton");

    const customerProfileModal =
        document.getElementById("customerProfileModal");

    const closeCustomerProfile =
        document.getElementById("closeCustomerProfile");


    if (customerProfileButton) {

        customerProfileButton.addEventListener(
            "click",
            function () {

                openModal(customerProfileModal);

            }
        );

    }


    if (closeCustomerProfile) {

        closeCustomerProfile.addEventListener(
            "click",
            function () {

                closeModal(customerProfileModal);

            }
        );

    }


    // =========================================================
    // CUSTOMER EDIT PROFILE
    // =========================================================

    const customerEditProfileButton =
        document.getElementById("customerEditProfileButton");

    const customerEditProfileModal =
        document.getElementById("customerEditProfileModal");

    const closeCustomerEditProfile =
        document.getElementById("closeCustomerEditProfile");


    if (customerEditProfileButton) {

        customerEditProfileButton.addEventListener(
            "click",
            function () {

                closeModal(customerProfileModal);

                openModal(customerEditProfileModal);

            }
        );

    }


    if (closeCustomerEditProfile) {

        closeCustomerEditProfile.addEventListener(
            "click",
            function () {

                closeModal(customerEditProfileModal);

            }
        );

    }


    // =========================================================
    // CUSTOMER ORDERS
    // =========================================================

    const customerOrdersButton =
        document.getElementById("customerOrdersButton");

    const customerOrdersButtonModal =
        document.getElementById("customerOrdersButtonModal");

    const customerOrdersModal =
        document.getElementById("customerOrdersModal");

    const closeCustomerOrders =
        document.getElementById("closeCustomerOrders");


    if (customerOrdersButton) {

        customerOrdersButton.addEventListener(
            "click",
            function () {

                openModal(customerOrdersModal);

            }
        );

    }


    if (customerOrdersButtonModal) {

        customerOrdersButtonModal.addEventListener(
            "click",
            function () {

                closeModal(customerProfileModal);

                openModal(customerOrdersModal);

            }
        );

    }


    if (closeCustomerOrders) {

        closeCustomerOrders.addEventListener(
            "click",
            function () {

                closeModal(customerOrdersModal);

            }
        );

    }


    // =========================================================
    // BOOKING MODAL
    // =========================================================

    const bookingModal =
        document.getElementById("bookingModal");

    const closeBooking =
        document.getElementById("closeBooking");

    const professionalId =
        document.getElementById("professionalId");

    const bookingProfessionalName =
        document.getElementById("bookingProfessionalName");

    const bookingDate =
        document.getElementById("bookingDate");

    const timeSlot =
        document.getElementById("timeSlot");

    const slotMessage =
        document.getElementById("slotMessage");

    const bookButtons =
        document.querySelectorAll(".book-now-btn");


    // =========================================================
    // TOMORROW AS MINIMUM BOOKING DATE
    // =========================================================

    function getTomorrow() {

        const today = new Date();

        today.setDate(
            today.getDate() + 1
        );

        const year =
            today.getFullYear();

        const month =
            String(
                today.getMonth() + 1
            ).padStart(2, "0");

        const day =
            String(
                today.getDate()
            ).padStart(2, "0");

        return `${year}-${month}-${day}`;
    }


    if (bookingDate) {

        bookingDate.min = getTomorrow();

    }


    // =========================================================
    // RESET TIME SLOTS
    // =========================================================

    function resetTimeSlots() {

        if (!timeSlot) {
            return;
        }

        Array.from(
            timeSlot.options
        ).forEach(function (option) {

            option.disabled = false;

            option.textContent =
                option.value ||
                "Select Time Slot";

        });


        timeSlot.value = "";


        if (slotMessage) {

            slotMessage.textContent = "";

            slotMessage.className =
                "slot-message";

        }

    }


    // =========================================================
    // CHECK BOOKED SLOTS
    // =========================================================

    async function checkBookedSlots() {

        if (
            !professionalId ||
            !bookingDate ||
            !timeSlot
        ) {
            return;
        }


        const professional =
            professionalId.value;

        const date =
            bookingDate.value;


        if (!professional || !date) {

            resetTimeSlots();

            return;
        }


        resetTimeSlots();


        const bookButton =
            document.querySelector(
                `.book-now-btn[data-professional-id="${professional}"]`
            );


        let url = "/order/booked-slots/";


        if (bookButton) {

            const customUrl =
                bookButton.dataset.bookedSlotsUrl;

            if (customUrl) {
                url = customUrl;
            }

        }


        const finalUrl =
            `${url}?professional_id=${encodeURIComponent(
                professional
            )}&booking_date=${encodeURIComponent(
                date
            )}`;


        try {

            const response =
                await fetch(finalUrl, {
                    method: "GET",
                    headers: {
                        "X-Requested-With": "XMLHttpRequest"
                    }
                });


            if (!response.ok) {

                throw new Error(
                    "Unable to check availability."
                );

            }


            const data =
                await response.json();


            const bookedSlots =
                data.booked_slots || [];


            bookedSlots.forEach(
                function (bookedSlot) {

                    const option =
                        Array.from(
                            timeSlot.options
                        ).find(
                            function (item) {
                                return (
                                    item.value ===
                                    bookedSlot
                                );
                            }
                        );


                    if (option) {

                        option.disabled = true;

                        option.textContent =
                            `${bookedSlot} - Already Booked`;

                    }

                }
            );


            if (bookedSlots.length > 0) {

                if (slotMessage) {

                    slotMessage.textContent =
                        "Some time slots are already booked.";

                    slotMessage.className =
                        "slot-message warning";

                }

            }


            const availableSlots =
                Array.from(
                    timeSlot.options
                ).filter(
                    function (option) {

                        return (
                            option.value &&
                            !option.disabled
                        );

                    }
                );


            if (availableSlots.length === 0) {

                if (slotMessage) {

                    slotMessage.textContent =
                        "All time slots are booked for this date. Please choose another date.";

                    slotMessage.className =
                        "slot-message error";

                }

            }

        } catch (error) {

            console.error(
                "Availability error:",
                error
            );

            if (slotMessage) {

                slotMessage.textContent =
                    "Unable to check availability. Please try again.";

                slotMessage.className =
                    "slot-message error";

            }

        }

    }


    // =========================================================
    // OPEN BOOKING
    // =========================================================

    bookButtons.forEach(
        function (button) {

            button.addEventListener(
                "click",
                function () {

                    const id =
                        button.dataset.professionalId;

                    const name =
                        button.dataset.professionalName;


                    if (professionalId) {

                        professionalId.value = id;

                    }


                    if (bookingProfessionalName) {

                        bookingProfessionalName.textContent =
                            name;

                    }


                    resetTimeSlots();


                    if (bookingDate) {

                        bookingDate.min =
                            getTomorrow();

                        bookingDate.value = "";

                    }


                    openModal(bookingModal);

                }
            );

        }
    );


    // =========================================================
    // DATE CHANGED
    // =========================================================

    if (bookingDate) {

        bookingDate.addEventListener(
            "change",
            function () {

                checkBookedSlots();

            }
        );

    }


    // =========================================================
    // CLOSE BOOKING
    // =========================================================

    if (closeBooking) {

        closeBooking.addEventListener(
            "click",
            function () {

                closeModal(bookingModal);

                resetTimeSlots();

            }
        );

    }


    // =========================================================
    // PROFESSIONAL PROFILE
    // =========================================================

    const professionalProfileButton =
        document.getElementById(
            "professionalProfileButton"
        );

    const professionalProfileModal =
        document.getElementById(
            "professionalProfileModal"
        );

    const closeProfessionalProfile =
        document.getElementById(
            "closeProfessionalProfile"
        );


    if (professionalProfileButton) {

        professionalProfileButton.addEventListener(
            "click",
            function () {

                openModal(
                    professionalProfileModal
                );

            }
        );

    }


    if (closeProfessionalProfile) {

        closeProfessionalProfile.addEventListener(
            "click",
            function () {

                closeModal(
                    professionalProfileModal
                );

            }
        );

    }


    // =========================================================
    // PROFESSIONAL EDIT PROFILE
    // =========================================================

    const professionalEditProfileButton =
        document.getElementById(
            "professionalEditProfileButton"
        );

    const professionalEditProfileModal =
        document.getElementById(
            "professionalEditProfileModal"
        );

    const closeProfessionalEditProfile =
        document.getElementById(
            "closeProfessionalEditProfile"
        );


    if (professionalEditProfileButton) {

        professionalEditProfileButton.addEventListener(
            "click",
            function () {

                closeModal(
                    professionalProfileModal
                );

                openModal(
                    professionalEditProfileModal
                );

            }
        );

    }


    if (closeProfessionalEditProfile) {

        closeProfessionalEditProfile.addEventListener(
            "click",
            function () {

                closeModal(
                    professionalEditProfileModal
                );

            }
        );

    }


    // =========================================================
    // PROFESSIONAL ORDERS
    // =========================================================

    const professionalOrdersButton =
        document.getElementById(
            "professionalOrdersButton"
        );

    const professionalOrdersButtonModal =
        document.getElementById(
            "professionalOrdersButtonModal"
        );

    const professionalOrdersModal =
        document.getElementById(
            "professionalOrdersModal"
        );

    const closeProfessionalOrders =
        document.getElementById(
            "closeProfessionalOrders"
        );


    if (professionalOrdersButton) {

        professionalOrdersButton.addEventListener(
            "click",
            function () {

                openModal(
                    professionalOrdersModal
                );

            }
        );

    }


    if (professionalOrdersButtonModal) {

        professionalOrdersButtonModal.addEventListener(
            "click",
            function () {

                closeModal(
                    professionalProfileModal
                );

                openModal(
                    professionalOrdersModal
                );

            }
        );

    }


    if (closeProfessionalOrders) {

        closeProfessionalOrders.addEventListener(
            "click",
            function () {

                closeModal(
                    professionalOrdersModal
                );

            }
        );

    }


    // =========================================================
    // CLOSE MODAL WHEN CLICKING OUTSIDE
    // =========================================================

    document.querySelectorAll(
        ".custom-modal"
    ).forEach(
        function (modal) {

            modal.addEventListener(
                "click",
                function (event) {

                    if (
                        event.target === modal
                    ) {

                        closeModal(modal);

                    }

                }
            );

        }
    );


    // =========================================================
    // ESCAPE KEY
    // =========================================================

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Escape") {

                document
                    .querySelectorAll(
                        ".custom-modal.show"
                    )
                    .forEach(
                        function (modal) {

                            closeModal(modal);

                        }
                    );

            }

        }
    );

});


/* =========================================================
   REGISTER PAGE
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    const accountType = document.getElementById("accountType");
    const professionalFields = document.getElementById("professionalFields");

    if (accountType && professionalFields) {

        function toggleProfessionalFields() {

            if (accountType.value === "Professional") {

                professionalFields.classList.add("active");

            } else {

                professionalFields.classList.remove("active");

            }
        }

        accountType.addEventListener(
            "change",
            toggleProfessionalFields
        );

        toggleProfessionalFields();
    }


    /* =====================================================
       REGISTER FORM VALIDATION
       ===================================================== */

    const registerForm = document.getElementById("registerForm");

    if (registerForm) {

        registerForm.addEventListener("submit", function (event) {

            const password =
                document.getElementById("password");

            const confirmPassword =
                document.getElementById("confirmPassword");

            if (
                password &&
                confirmPassword &&
                password.value !== confirmPassword.value
            ) {

                event.preventDefault();

                alert("Passwords do not match.");

                confirmPassword.focus();
            }

        });
    }

});