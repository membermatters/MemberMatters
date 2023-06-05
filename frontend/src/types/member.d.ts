enum MemberState {
  noob = "Needs Induction",
  active = "Active",
  inactive = "Inactive",
  accountonly = "Account Only",
}

enum MemberSubscriptionState {
  inactive = "Inactive",
  active = "Active",
  cancelling = "Cancelling",
}

interface MemberProfile {
  id: number;
  admin: boolean;
  superuser: boolean;
  email: string;
  registrationDate: string;
  lastUpdatedProfile: string;
  screenName: string;
  name: {
    first: string;
    last: string;
    full: string;
  };
  phone: string;
  state: MemberState;
  vehicleRegistrationPlate: string;
  rfid: string;
  memberBucks: {
    balance: number;
    lastPurchase: string | null;
  };
  updateProfileRequired: boolean;
  lastSeen: string | null;
  lastInduction: string | null;
  stripe: {
    cardExpiry: string;
    last4: string;
  };
  subscriptionStatus: MemberSubscriptionState;
}
